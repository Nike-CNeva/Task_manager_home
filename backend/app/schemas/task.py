from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.enums import MaterialFormEnum, MaterialThicknessEnum, MaterialTypeEnum, StatusEnum, UrgencyEnum



class TaskBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quantity: Optional[int] = Field(None, description="Количество")
    urgency: UrgencyEnum = Field(..., description="Срочность")
    status: StatusEnum = Field(..., description="Статус")
    waste: Optional[str] = Field(None, description="Отходы")
    weight: Optional[str] = Field(None, description="Вес")
    created_at: datetime = Field(..., description="Дата создания")
    completed_at: Optional[datetime] = Field(None, description="Дата завершения")


class TaskRead(TaskBase):
    id: int = Field(..., description="ID задачи")



class TaskCreate(BaseModel):
    """
    Схема для создания задачи в рамках заявки.
    """
    product_name: str = Field(..., description="имя продукта")
    product_details: Dict[str, Any] = Field(..., description="Детали продукта")
    material_form: MaterialFormEnum = Field(..., description="Форма материала")
    material_type: MaterialTypeEnum = Field(..., description="Тип материала")
    color: str = Field(..., description="Цвет материала")
    painting: bool = Field(..., description="Нужна ли покраска")
    material_thickness: MaterialThicknessEnum = Field(..., description="Толщина материала")
    sheets: Optional[List[Dict[str, int]]] = Field(None, description="Листы")
    urgency: UrgencyEnum = Field(..., description="Срочность")
    workshops: List[str] = Field(..., description="Рабочие места")
    employees: List[int] = Field(..., description="Сотрудники")
