from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.task import TaskCreateResponse, TaskRead


class BidBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_number: Optional[str] = Field(None, description="Номер заявки")
    manager: str = Field(..., description="Менеджер")


class BidRead(BidBase):
    id: int = Field(..., description="ID заявки")

class BidWithTasks(BidRead):
    tasks: List[TaskRead] = Field(default_factory=list, description="Список задач в заявке")

class BidCreateResponse(BaseModel):
    """
    Схема для создания заявки.
    """
    customer_id: int = Field(..., description="ID заказчика")
    manager: str = Field(..., description="Менеджер")
    status: str = Field(..., description="Статус")
    comment: Optional[str] = Field(None, description="Комментарий к заявке")
    tasks: List[TaskCreateResponse] = Field(..., description="Список задач")
