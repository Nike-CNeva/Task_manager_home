
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.user import UserRead




class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    content: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")
    user: UserRead = Field(..., description="Пользователь, оставивший комментарий")




class CommentRead(CommentBase):
    id: int = Field(..., description="ID комментария")


class CommentPayload(BaseModel):
    content: str
    bid_id: int
    
class CommentCreate(CommentPayload):
    user_id: int


class CommentResponse(BaseModel):
    id: int
    user: UserRead
    content: str
    created_at: datetime