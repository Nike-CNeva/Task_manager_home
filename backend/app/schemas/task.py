from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ManagerEnum, MaterialThicknessEnum, MaterialTypeEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum, UrgencyEnum, WorkshopEnum


class TaskWorkshopRead(BaseModel):
    workshop_name: WorkshopEnum
    status: StatusEnum

class CustomerShort(BaseModel):
    id: int
    name: str

class ProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    profile_type: ProfileTypeEnum
    length: int

class CassetteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cassette_type: CassetteTypeEnum
    description: str | None = None

class KlamerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    klamer_type: KlamerTypeEnum

class BracketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    width: int
    length: str

class ExtensionBracketRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    width: int
    length: str
    heel: bool

class LinearPanelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field: int
    rust: int
    length: int
    butt_end: bool

class ProductTRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type: ProductTypeEnum  # Или ProductTypeEnum если ты хочешь enum
    profile: ProfileRead | None = None
    cassette: CassetteRead | None = None
    klamer: KlamerRead | None = None
    bracket: BracketRead | None = None
    extension_bracket: ExtensionBracketRead | None = None
    linear_panel: LinearPanelRead | None = None


class MaterialReadShort(BaseModel):
    id: int
    type: MaterialTypeEnum
    color: str
    thickness: MaterialThicknessEnum
    painting: bool

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product: ProductTRead
    material: MaterialReadShort
    quantity: int
    urgency: UrgencyEnum
    status: StatusEnum
    waste: Optional[str]
    weight: Optional[str]
    sheets: Optional[List[Dict[str, int]]]
    created_at: datetime
    completed_at: Optional[datetime]
    workshops: Optional[List[TaskWorkshopRead]]
    product_fields: List[Dict[str, Any]]

class BidRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    task_number: int
    manager: ManagerEnum
    customer: CustomerShort
    tasks: List[TaskRead]



class TaskCreate(BaseModel):
    """
    Схема для создания задачи в рамках заявки.
    """
    product_name: str = Field(..., description="имя продукта")
    product_details: Dict[str, Any] = Field(..., description="Детали продукта")
    material_type: MaterialTypeEnum = Field(..., description="Тип материала")
    color: str = Field(..., description="Цвет материала")
    painting: bool = Field(..., description="Нужна ли покраска")
    material_thickness: MaterialThicknessEnum = Field(..., description="Толщина материала")
    sheets: Optional[List[Dict[str, int]]] = Field(None, description="Листы")
    urgency: UrgencyEnum = Field(..., description="Срочность")
    workshops: List[str] = Field(..., description="Рабочие места")
    employees: List[int] = Field(..., description="Сотрудники")
