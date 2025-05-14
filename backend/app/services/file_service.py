import aiofiles
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile

from backend.app.core.settings import settings
from backend.app.database.database_service import AsyncDatabaseService
import logging

from backend.app.models.files import Files

logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.UPLOAD_DIR

async def save_file(task_id: int, file: UploadFile, file_type: str, db: AsyncSession) -> Files:
    """Асинхронно сохраняет файл и создает запись в базе данных."""
    db_service = AsyncDatabaseService(db)
    task_folder = UPLOAD_DIR / str(task_id)
    task_folder.mkdir(parents=True, exist_ok=True)
    file_path = task_folder / file.filename

    try:
        async with aiofiles.open(file_path, "wb") as out_file:
            while content := await file.read(1024):  # читаем кусками по 1024 байта
                await out_file.write(content)
    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

    task_file_data = {
        "task_id": task_id,
        "file_path": str(file_path),
        "file_type": file_type
    }

    task_file = await db_service.create(Files, task_file_data)
    return task_file

async def get_files_for_task(db: AsyncSession, task_id: int) -> list[Files]:
    """Асинхронно получает список файлов для задачи."""
    db_service = AsyncDatabaseService(db)
    result = await db.execute(
        db_service.select(Files).filter(Files.task_id == task_id)
    )
    return result.scalars().all()

async def delete_files(task_id: int, file_id: int, db: AsyncSession):
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
