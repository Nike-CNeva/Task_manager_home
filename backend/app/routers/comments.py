from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_db
from backend.app.schemas.comment import CommentCreate, CommentResponse
from backend.app.services import comment_service
from datetime import datetime

router = APIRouter()

@router.post("/tasks/{task_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_task_comment(task_id: int, comment_data: CommentCreate, db: AsyncSession = Depends(get_db)):
    comment = await comment_service.add_comment(db, task_id, comment_data.user_id, comment_data.content)
    return comment

@router.get("/tasks/{task_id}/")
async def list_task_comments(task_id: int, db: AsyncSession = Depends(get_db)):
    try:
        comments = await comment_service.get_comments_for_task(db, task_id)
        comment_list: List[Dict[str, str]] = [
            {
                "user": comment.user.username,  # или нужное поле пользователя
                "content": comment.content,
                "created_at": datetime.now().isoformat()
            }
            for comment in comments
        ]
        return JSONResponse(content=comment_list)
    except Exception as e:
        # Можно добавить логирование ошибки
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))