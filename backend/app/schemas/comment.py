
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")
    is_read: bool = Field(False, description="Прочитан ли комментарий")
    is_deleted: bool = Field(False, description="Удален ли комментарий")


class CommentRead(CommentBase):
    id: int = Field(..., description="ID комментария")


class CommentCreate(BaseModel):
    user_id: int
    content: str
    task_id: int
    

class CommentResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    content: str
    created_at: datetime