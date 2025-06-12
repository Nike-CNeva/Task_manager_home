import mimetypes
from urllib.parse import quote
import os
import shutil
from zipfile import ZipFile
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_db
from backend.app.models.files import Files
from backend.app.schemas.file import UploadedFileResponse
from backend.app.services import file_service
from sqlalchemy.future import select
from starlette.requests import Request
import logging
logger = logging.getLogger(__name__)

router = APIRouter()
# Список MIME, которые мы считаем поддерживаемыми для inline просмотра
INLINE_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "text/plain",
    "text/html",
    "audio/mpeg",
    "audio/ogg",
    "video/mp4",
    "video/webm",
    # можно добавить ещё нужные форматы
}
@router.post(
    "/bid/{bid_id}/upload",
    response_model=UploadedFileResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузка файла к задаче",
    description="Загружает файл и прикрепляет его к задаче"
)
async def upload_bid_file(
    bid_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> UploadedFileResponse:
    try:
        saved_file: Files = await file_service.save_file(bid_id, file, db)
        return UploadedFileResponse(
            filename=saved_file.filename,
            file_path=saved_file.file_path,
            bid_id=bid_id,
            file_type=saved_file.file_type
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка при загрузке файла{e}") 
       
@router.get("/bid/{bid_id}/")
async def list_bid_files(bid_id: int, db: AsyncSession = Depends(get_db)):
    try:
        files = await file_service.get_files_for_bid(db, bid_id)
        file_list = [{"filename": file.filename, "file_type": file.file_type} for file in files]
        return JSONResponse(content=file_list)
    except Exception as e:
        # logger.error(f"Error fetching files: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
       

@router.get("/uploads/{bid_id}/{file_name}")
async def serve_file(bid_id: int, file_name: str, request: Request):
    file_path = f"/app/uploads/{bid_id}/{file_name}"  # скорректируйте путь под себя

    if not os.path.isfile(file_path):
        return {"error": "Файл не найден"}

    # Определяем MIME-тип по расширению
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = "application/octet-stream"

    # Кодируем имя файла для заголовка Content-Disposition в RFC5987
    encoded_file_name = quote(file_name)
    
    # Для файлов, которые должны открываться в браузере, используем inline
    # Для остальных — attachment (принудительная загрузка)
    # Можно настроить логику, например, список расширений для inline
    browser_inline_ext = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf', 'txt', 'html', 'mp4', 'webm', 'ogg', 'mp3'}
    ext = file_name.split('.')[-1].lower()
    logger.info(f"Filename: {file_name}, ext: {ext}")

    disposition_type = "inline" if ext in browser_inline_ext else "attachment"
    logger.info(f"Content-Disposition: {disposition_type}")

    content_disposition = f"{disposition_type}; filename*=UTF-8''{encoded_file_name}"

    headers = {
        "Content-Disposition": content_disposition
    }

    return FileResponse(
        path=file_path,
        media_type=mime_type,
        headers=headers,
        filename=file_name
    )

@router.delete("/files/{file_id}")
async def delete_file(file_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Files).where(Files.id == file_id))
    file = result.scalar_one_or_none()

    if not file:
        raise HTTPException(status_code=404, detail="Файл не найден")

    # Удаление физического файла
    if file.file_path and os.path.exists(file.file_path):
        os.remove(file.file_path)

    await db.delete(file)
    await db.commit()

    return {"detail": "Файл удалён"}

@router.get("/tasks/{bid_id}/files/zip")
async def download_files_zip(bid_id: int, db: AsyncSession = Depends(get_db)):
    # Путь к временной папке и zip-файлу
    zip_path = f"temp/task_{bid_id}_files.zip"
    temp_dir = f"temp/task_{bid_id}_files"
    os.makedirs(temp_dir, exist_ok=True)

    # Скопировать файлы задачи во временную папку
    files = await file_service.get_files_for_bid(db, bid_id)  # реализуй сам
    for f in files:
        shutil.copy(f.file_path, os.path.join(temp_dir, f.filename))

    # Создать архив
    with ZipFile(zip_path, 'w') as zipf:
        for filename in os.listdir(temp_dir):
            zipf.write(os.path.join(temp_dir, filename), arcname=filename)

    # Очистка временной папки можно делать через фоновую задачу
    return FileResponse(zip_path, filename=os.path.basename(zip_path))
