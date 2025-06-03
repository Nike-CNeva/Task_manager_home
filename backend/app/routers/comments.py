from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.models.comment import Comment
from backend.app.schemas.comment import CommentPayload, CommentResponse
from backend.app.services import comment_service
from datetime import datetime

router = APIRouter()

@router.post("/tasks/{bid_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_task_comment(comment_data: CommentPayload, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    comment = await comment_service.add_comment(db, comment_data.bid_id, current_user.id, comment_data.content)
    return comment

@router.delete("/comments/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Находим комментарий
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()

        if comment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Комментарий не найден")

        # Удаляем комментарий
        await db.delete(comment)
        await db.commit()

        return {"message": "Комментарий успешно удалён"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))