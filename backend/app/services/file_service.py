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
from backend.app.models.files import Files

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


async def save_file(bid_id: int, file: UploadFile, db: AsyncSession) -> Files:
    db_service = AsyncDatabaseService(db)
    bid_folder = UPLOAD_DIR / str(bid_id)
    bid_folder.mkdir(parents=True, exist_ok=True)
    filename = file.filename
    if not filename:
        raise HTTPException(status_code=400, detail="Имя файла не может быть пустым")

    file_path = bid_folder / filename

    # Определяем тип файла по расширению
    file_type_enum = await get_file_type_by_extension(filename)
    if not file_type_enum:
        raise HTTPException(status_code=400, detail="Неизвестный тип файла")

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

async def delete_files(file_id: int, db: AsyncSession):
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
