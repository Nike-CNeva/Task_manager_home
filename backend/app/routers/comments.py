from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.schemas.comment import CommentCreate, CommentResponse
from backend.app.services import comment_service
from datetime import datetime

router = APIRouter()

@router.post("/tasks/{bid_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_task_comment(comment_data: CommentCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    comment = await comment_service.add_comment(db, comment_data.bid_id, comment_data.user_id, comment_data.content)
    return comment

@router.get("/tasks/{bid_id}/")
async def list_task_comments(bid_id: int, db: AsyncSession = Depends(get_db)):
    try:
        comments = await comment_service.get_comments_for_task(db, bid_id)
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