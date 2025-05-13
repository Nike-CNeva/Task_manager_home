from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import StatusEnum
from backend.app.schemas.user import UserRead


class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantity: Optional[int] = Field(None, description="Количество")
    urgency_id: StatusEnum = Field(..., description="Срочность")
    status_id: StatusEnum = Field(..., description="Статус")
    waste: Optional[str] = Field(None, description="Отходы")
    weight: Optional[str] = Field(None, description="Вес")
    created_at: datetime = Field(..., description="Дата создания")
    completed_at: Optional[datetime] = Field(None, description="Дата завершения")


class TaskRead(TaskBase):
    id: int = Field(..., description="ID задачи")


class TaskWithUsers(TaskRead):
    responsible_users: List[UserRead] = Field(default_factory=list, description="Список ответственных пользователей")

class TaskCreateRequest(BaseModel):
    """
    Схема для создания задачи в рамках заявки.
    """
    product_id: str = Field(..., description="ID продукта")
    product_name: str = Field(..., description="Название продукта")
    count: int = Field(..., description="Количество")
    material_form: str = Field(..., description="Форма материала")
    material_type: str = Field(..., description="Тип материала")
    material_color: str = Field(..., description="Цвет материала")
    material_thickness: Optional[str] = Field(None, description="Толщина материала")
    material_width: Optional[str] = Field(None, description="Ширина материала")
    material_length: Optional[str] = Field(None, description="Длина материала")
    comment: Optional[str] = Field(None, description="Комментарий к задаче")
    fields: Optional[Dict[str, Any]] = Field(None, description="Дополнительные поля")
