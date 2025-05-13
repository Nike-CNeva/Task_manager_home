from sqlalchemy.orm import Session
from backend.app.models.models import Comment
from typing import List
from backend.app.database.database_service import DatabaseService
import logging

logger = logging.getLogger(__name__)

def add_comment(db: Session, task_id: int, user_id: int, content: str) -> Comment:
    """Добавляет комментарий к задаче."""
    db_service = DatabaseService(db)
    comment_data = {
        "task_id": task_id,
        "comment": content,
        "user_id": user_id
    }
    comment = db_service.create(Comment, comment_data)
    return comment

def get_comments_for_task(db: Session, task_id: int) -> List[Comment]:
    """Получает список комментариев для задачи."""
    db_service = DatabaseService(db)
    return db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()
