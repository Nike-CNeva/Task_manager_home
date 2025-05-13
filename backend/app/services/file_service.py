import shutil
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from backend.app.models.models import Files
from backend.app.core.settings import settings
from backend.app.database.database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = settings.UPLOAD_DIR

def save_file(task_id: int, file: UploadFile, file_type: str, db: Session) -> Files:
    """Сохраняет файл и создает запись в базе данных."""
    db_service = DatabaseService(db)
    task_folder = UPLOAD_DIR / str(task_id)
    task_folder.mkdir(parents=True, exist_ok=True)
    file_path = task_folder / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Ошибка при сохранении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при сохранении файла")

    task_file_data = {
        "task_id": task_id,
        "file_path": str(file_path),
        "file_type": file_type
    }
    task_file = db_service.create(Files, task_file_data)
    return task_file

def get_files_for_task(db: Session, task_id: int) -> list[Files]:
    """Получает список файлов для задачи."""
    db_service = DatabaseService(db)
    return db.query(Files).filter(Files.task_id == task_id).all()

def delete_files(task_id: int, file_id: int, db: Session):
    """Удаляет файл и запись в базе данных."""
    db_service = DatabaseService(db)
    file = db_service.get_by_id(Files, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")
    file_path = Path(file.file_path)
    try:
        if file_path.exists():
            file_path.unlink()
    except Exception as e:
        logger.error(f"Ошибка при удалении файла: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при удалении файла")
    db_service.delete(Files, file_id)
