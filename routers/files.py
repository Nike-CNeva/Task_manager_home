from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from services import file_service

router = APIRouter()

@router.post("/tasks/{task_id}/upload")
async def upload_task_file(task_id: int, file: UploadFile = File(...), file_type: str = "default", db: Session = Depends(get_db)):
    try:
        saved_file = await file_service.save_file(task_id, file, file_type, db)
        return JSONResponse(content={
            "filename": saved_file.filename,
            "task_id": task_id,
            "file_type": file_type
        }, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        # Consider logging the error here: logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/tasks/{task_id}/")
def list_task_files(task_id: int, db: Session = Depends(get_db)):
    try:
        files = file_service.get_files_for_task(db, task_id)
        file_list = [{"filename": file.filename, "file_type": file.file_type} for file in files]
        return JSONResponse(content=file_list)
    except Exception as e:
        # Consider logging the error here: logger.error(f"Error fetching files: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/tasks/{task_id}/{file_id}/delete")
def delete_task_file(task_id: int, file_id: int, db: Session = Depends(get_db)):
    try:
        file_service.delete_files(task_id, file_id, db)
        return JSONResponse(content={"message": "Файл успешно удален"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
