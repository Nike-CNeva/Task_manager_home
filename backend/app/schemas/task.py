from datetime import datetime
from token import OP
from typing import Any, Dict, List, Literal, Optional, Union
from unittest.mock import Base
from pydantic import BaseModel, ConfigDict, Field
from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ManagerEnum, MaterialThicknessEnum, MaterialTypeEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum, UrgencyEnum, WorkshopEnum
from pydantic import field_validator

from backend.app.schemas.comment import CommentRead

class TaskWorkshopRead(BaseModel):
    workshop_name: WorkshopEnum
    status: StatusEnum
    progress_percent: float


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
    waste: Optional[float] = None
    weight: Optional[float] = None


class TaskProductRead(BaseModel):
    product: ProductTRead
    color: Optional[str]
    painting: bool
    quantity: int
    description: Optional[str] = None
    done_quantity: int
    product_fields: List[Dict[str, Any]]


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    material: MaterialReadShort
    urgency: UrgencyEnum
    status: StatusEnum
    sheets: Optional[List[Dict[str, int]]]
    created_at: datetime
    completed_at: Optional[datetime]
    workshops: Optional[List[TaskWorkshopRead]]
    task_products: List[TaskProductRead]
    total_quantity: int
    done_quantity: int
    progress_percent: float

class FilesRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    bid_id: int
    filename: str
    file_type: str
    file_path: str

class BidRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    task_number: int
    manager: ManagerEnum
    customer: CustomerShort
    status: StatusEnum
    tasks: List[TaskRead]
    comments: List[CommentRead] = []
    progress_percent: Optional[float] = None
    files: Optional[List[FilesRead]] = None





class MaterialCreateSchema(BaseModel):
    """
    Схема для создания материала.
    """
    material_type: str = Field(..., description="Тип материала")
    material_thickness: str = Field(..., description="Толщина материала")
    color: Optional[str] = Field(None, description="Цвет материала")

class SheetsCreate(BaseModel):
    """
    Схема для создания информации о листах для задачи.
    """
    width: int = Field(..., description="Ширина листа")
    length: int = Field(..., description="Длина листа")
    quantity: int = Field(..., description="Количество листов")
    task_id: Optional[int] = Field(None, description="ID задачи")


class CommonProductFields(BaseModel):
    quantity: int = Field(..., description="Количество")
    color: Optional[str] = Field(None, description="Цвет")
    painting: Optional[bool] = Field(False, description="Покраска")
    description: Optional[str] = Field(None, description="Описание")


class CassetteProduct(CommonProductFields):
    cassette_type: str

class ProfileProduct(CommonProductFields):
    profile_type: str
    length: float

class KlamerProduct(CommonProductFields):
    klamer_type: str

class BracketProduct(CommonProductFields):
    width: float
    length: str

class ExtensionBracketProduct(CommonProductFields):
    width: float
    length: str
    has_heel: bool

class LinearPanelProduct(CommonProductFields):
    field: float
    rust: float
    length: float
    butt_end: Optional[bool] = False


class SheetProduct(CommonProductFields):
    pass



ProductDetail = Union[
    CassetteProduct,
    ProfileProduct,
    KlamerProduct,
    BracketProduct,
    ExtensionBracketProduct,
    LinearPanelProduct,
    SheetProduct
]
class TaskCreate(BaseModel):
    """
    Схема для создания задачи в рамках заявки.
    """
    product_name: str = Field(..., description="имя продукта")
    product_details: list[Any] = Field(..., description="Детали продукта")
    material: MaterialCreateSchema = Field(..., description="материал")
    sheets: Optional[List[SheetsCreate]] = Field(None, description="Листы")
    urgency: UrgencyEnum = Field(..., description="Срочность")
    workshops: List[str] = Field(..., description="Рабочие места")
    employees: List[int] = Field(..., description="Сотрудники")

    @field_validator("product_details", mode="before")
    @classmethod
    def detect_product_type(cls, value):
        def classify_product(obj: dict) -> ProductDetail:
            if "cassette_type" in obj:
                return CassetteProduct(**obj)
            elif "profile_type" in obj:
                return ProfileProduct(**obj)
            elif "klamer_type" in obj:
                return KlamerProduct(**obj)
            elif "width" in obj and "length" in obj and "has_heel" in obj:
                return ExtensionBracketProduct(**obj)
            elif "width" in obj and "length" in obj:
                return BracketProduct(**obj)
            elif "panel_width" in obj:
                return LinearPanelProduct(**obj)
            else:
                return SheetProduct(**obj)

        return [classify_product(item) for item in value]
    
class MaterialUpdate(BaseModel):
    weight: Optional[float] = None
    waste: Optional[float] = None

class QuantityItem(BaseModel):
    product_id: int
    quantity: int

class QuantityUpdateRequest(BaseModel):
    task_id: int
    quantities: List[QuantityItem]