from typing import List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.comment import Comment
from backend.app.database.database_service import AsyncDatabaseService
import logging

from backend.app.schemas.comment import CommentCreate, CommentRead


logger = logging.getLogger(__name__)

async def add_comment(db: AsyncSession, bid_id: int, user_id: int, content: str) -> CommentRead:
    db_service = AsyncDatabaseService(db)

    comment_data = CommentCreate(
        user_id=user_id,
        content=content,
        bid_id=bid_id
    ).model_dump()

    # Создаём комментарий
    comment = await db_service.create(Comment, comment_data)

    # Дозагружаем пользователя
    stmt = (
        select(Comment)
        .options(joinedload(Comment.user))  # подтягиваем user
        .where(Comment.id == comment.id)
    )
    result = await db.execute(stmt)
    comment_with_user = result.scalar_one()

    # Возвращаем сериализованную модель CommentRead
    return CommentRead.model_validate(comment_with_user)

async def get_comments_for_task(db: AsyncSession, bid_id: int) -> List[Comment]:
    """Получает список комментариев для задачи."""
    result = await db.execute(
        select(Comment)
        .where(Comment.bid_id == bid_id)
        .order_by(Comment.created_at.desc())
    )
    comments = list(result.scalars().all())
    return comments