from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_db
from backend.app.models.files import Files
from backend.app.schemas.file import UploadedFileResponse
from backend.app.services import file_service

router = APIRouter()

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
       
@router.delete("/bids/{file_id}/delete")
async def delete_bid_file(file_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await file_service.delete_files(file_id, db)
        return JSONResponse(content={"message": "Файл успешно удален"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
