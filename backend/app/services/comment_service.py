from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.comment import Comment
from backend.app.database.database_service import AsyncDatabaseService
import logging

from backend.app.schemas.comment import CommentCreate


logger = logging.getLogger(__name__)

async def add_comment(db: AsyncSession, task_id: int, user_id: int, content: str) -> Comment:
    db_service = AsyncDatabaseService(db)
    
    comment_data = CommentCreate(
        user_id=user_id,
        content=content,
        task_id=task_id
    ).model_dump()
    
    comment = await db_service.create(Comment, comment_data)
    return comment

async def get_comments_for_task(db: AsyncSession, task_id: int) -> List[Comment]:
    """Получает список комментариев для задачи."""
    result = await db.execute(
        select(Comment)
        .where(Comment.bid_id == task_id)
        .order_by(Comment.created_at.desc())
    )
    comments = list(result.scalars().all())
    return comments