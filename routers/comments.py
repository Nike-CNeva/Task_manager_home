from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from services import comment_service

router = APIRouter()

@router.post("/tasks/{task_id}/", response_model=dict)
def add_task_comment(task_id: int, user_id: int, content: str, db: Session = Depends(get_db)):
    comment = comment_service.add_comment(db, task_id, user_id, content)
    return JSONResponse(content={
        "id": comment.id,
        "user_id": comment.user_id,
        "task_id": comment.task_id,
        "content": comment.content,
        "created_at": comment.created_at
    }, status_code=status.HTTP_201_CREATED)

@router.get("/tasks/{task_id}/")
def list_task_comments(task_id: int, db: Session = Depends(get_db)):
    try:
        comments = comment_service.get_comments_for_task(db, task_id)
        comment_list = [{"user": comment.user, "content": comment.content, "created_at": comment.created_at} for comment in comments]
        return JSONResponse(content=comment_list)
    except Exception as e:
        # Consider logging the error here: logger.error(f"Error fetching comments: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
