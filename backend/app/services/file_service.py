from typing import Any, Dict, Sequence
import aiofiles
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from backend.app.core.settings import settings
from backend.app.database.database_service import AsyncDatabaseService
import logging
from backend.app.models.enums import FileType
from backend.app.models.files import ClampLocations, Files, NestFile, Parts, Tools
import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path
from PIL import Image, ImageEnhance
import io
import json


logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.UPLOAD_DIR
# Словарь с расширениями для типов
FILE_EXTENSIONS = {
    FileType.PHOTO: [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff"],
    FileType.IMAGE: [".svg", ".webp", ".heic", ".ico"],
    FileType.PDF: [".pdf"],
    FileType.NC: [".nc"],
    FileType.EXCEL: [".xls", ".xlsx", ".xlsm", ".csv"],
    FileType.WORD: [".doc", ".docx", ".rtf", ".odt"],
    FileType.DXF: [".dxf"],
    FileType.DWG: [".dwg"],
}

# Функция для определения типа файла по расширению
async def get_file_type_by_extension(filename: str) -> FileType | None:
    ext = filename.lower().rpartition('.')[-1]
    ext = '.' + ext if ext else ''
    for file_type, extensions in FILE_EXTENSIONS.items():
        if ext in extensions:
            return file_type


async def save_file(bid_id: int, file: UploadFile, db: AsyncSession, internal: bool = False) -> Files:
    db_service = AsyncDatabaseService(db)
    bid_folder = UPLOAD_DIR / str(bid_id)
    bid_folder.mkdir(parents=True, exist_ok=True)
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Имя файла не может быть пустым")

    file_path = bid_folder / filename

    # Определяем тип файла по расширению
    if not internal:
        file_type_enum = await get_file_type_by_extension(filename)
        if not file_type_enum:
            raise HTTPException(status_code=400, detail="Неизвестный тип файла")
    else:
        # Внутренние файлы можно сохранять с типом SYSTEM или аналогичным
        file_type_enum = FileType.SYSTEM

    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

    bid_file_data: Dict[str, Any] = {
        "bid_id": bid_id,
        "file_path": str(file_path),
        "file_type": file_type_enum.value,  # строковое значение enum
        "filename": file.filename
    }

    bid_file = await db_service.create(Files, bid_file_data)

    return bid_file

async def get_files_for_bid(db: AsyncSession, bid_id: int) -> Sequence[Files]:
    """Асинхронно получает список файлов для задачи."""
    stmt = select(Files).filter(Files.bid_id == bid_id)  # используем select из sqlalchemy
    result = await db.execute(stmt)
    return result.scalars().all()

async def delete_files(file_id: int, db: AsyncSession) -> str:
    """Асинхронно удаляет файл и запись в базе данных."""
    db_service = AsyncDatabaseService(db)
    file = await db_service.get_by_id(Files, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    file_path = Path(file.file_path)
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        logger.error(f"Ошибка при удалении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при удалении файла")
    
    await db_service.delete(Files, file_id)
    return "Файл успешно удалён"


async def extract_nest_data_and_image(file_path: str, db: AsyncSession) -> dict:
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    # === Сбор данных ===
    data = {
        "nest_id": None,
        "material": None,
        "thickness": None,
        "nc_file_name": None,
        "sheet_utilization": None,
        "sheet_size": None,
        "time_per_sheet": None,
        "nest_notes": None,
        "sheet_quantity": None,
        "clamp_1": None,
        "clamp_2": None,
        "clamp_3": None,
        "parts": [],
        "tools": [],
    }
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        lines = text.split("\n")

        for i, line in enumerate(lines):
            if "Nest ID" in line and "Material" in line:
                part = line.strip().split()
                data["nest_id"] = part[2]
                data["material"] = part[-2]
                data["thickness"] = part[-1]
            elif "NC File Name" in line and "Sheet Utilization" in line:
                part = line.strip().split()
                data["nc_file_name"] = part[3]
                data["sheet_utilization"]= part[-1]
            elif "Sheet Size" in line and "Time Per Sheet" in line:
                part = line.strip().split()
                data["sheet_size"] = part[2]
                data["time_per_sheet"] = part[-1]
            elif "Clamp Locations" in line:
                part = line.strip().split()
                data["clamp_1"] = part[2]
                data["clamp_2"] = part[3]
                data["clamp_3"] = part[4]
            elif "Nest Notes" in line:
                part = line.strip().split()
                data["nest_notes"] = part[2]
                data["sheet_quantity"] = part[-2]
            elif "Part name" in line:
                part_index = i + 1
                while part_index < len(lines) and lines[part_index].strip():
                    part_line = lines[part_index]
                    part_info = part_line.split()
                    if len(part_info) >= 4:
                        data["parts"].append({
                            "id": part_info[0],
                            "name": part_info[1],
                            "quantity": part_info[2],
                            "time_per_part": part_info[3],
                        })
                    part_index += 1
                    if part_index < len(lines) and "Tool Data" in lines[part_index]:
                        break
            elif "Station" in line and "Tool" in line:
                tool_index = i + 1
                while tool_index < len(lines) and lines[tool_index].strip():
                    tool_line = lines[tool_index]
                    tool_info = tool_line.split()
                    if len(tool_info) == 9:
                        station = f"{tool_info[0]} {tool_info[1]}"
                        size = f"{tool_info[3]} {tool_info[4]}"
                        data["tools"].append({
                            "station": station,
                            "tool": tool_info[2],
                            "size": size,
                            "angle": tool_info[5],
                            "die": tool_info[6],
                            "hits": tool_info[7],
                        })
                    elif len(tool_info) == 8:
                        station = f"{tool_info[0]} {tool_info[1]}"
                        data["tools"].append({
                            "station": station,
                            "tool": tool_info[2],
                            "size": tool_info[3],
                            "angle": tool_info[4],
                            "die": tool_info[5],
                            "hits": tool_info[6],
                        })
                    tool_index += 1

    doc = fitz.open(str(file_path))
    page = doc[0]
    crop_rect = fitz.Rect(63, 106, 461, 304)
    mat = fitz.Matrix(6, 6)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    sharp_img = ImageEnhance.Sharpness(img).enhance(5.0)

    # Создаём путь к system/ и файлы там сохраняем
    system_dir = file_path.parent / "system"
    system_dir.mkdir(parents=True, exist_ok=True)

    png_path = system_dir / (file_path.stem + ".png")

    sharp_img.save(png_path)

    # === Находим file_id в таблице files ===
    file_record = await db.execute(
        select(Files).where(Files.file_path == str(file_path))
    )
    file_obj = file_record.scalar_one_or_none()
    if not file_obj:
        raise Exception("Файл не найден в базе данных")

    # === Сохраняем NestFile ===
    nest_file = NestFile(
        file_id=file_obj.id,
        nest_id=int(data["nest_id"]),
        material=data["material"],
        thickness=data["thickness"],
        nc_file_name=data["nc_file_name"],
        sheet_utilization=float(data["sheet_utilization"].strip('%')),
        sheet_size=data["sheet_size"],
        time_per_sheet=data["time_per_sheet"],
        nest_notes=data["nest_notes"],
        sheet_quantity=int(data["sheet_quantity"]),
        nest_screen_file_path=str(png_path),
    )
    db.add(nest_file)
    await db.flush()  # Чтобы получить nest_file.id

    # === Сохраняем ClampLocations ===
    clamp = ClampLocations(
        nest_file_id=nest_file.id,
        clamp_1=int(data["clamp_1"].strip('1@')),
        clamp_2=int(data["clamp_2"].strip('2@')),
        clamp_3=int(data["clamp_3"].strip('3@'))
    )
    db.add(clamp)

    # === Сохраняем Parts ===
    for part in data["parts"]:
        db.add(Parts(
            nest_file_id=nest_file.id,
            part_id=int(part["id"]),
            name=part["name"],
            quantity=int(part["quantity"]),
            time_per_part=part["time_per_part"]
        ))

    # === Сохраняем Tools ===
    for tool in data["tools"]:
        db.add(Tools(
            nest_file_id=nest_file.id,
            station=tool["station"],
            tool=tool["tool"],
            size=tool["size"],
            angle=int(tool["angle"]),
            die=float(tool["die"]),
            hits=int(tool["hits"])
        ))

    return data



