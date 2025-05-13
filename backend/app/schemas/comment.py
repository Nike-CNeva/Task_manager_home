
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comment: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")
    is_read: bool = Field(False, description="Прочитан ли комментарий")
    is_deleted: bool = Field(False, description="Удален ли комментарий")


class CommentRead(CommentBase):
    id: int = Field(..., description="ID комментария")


