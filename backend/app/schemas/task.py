from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union
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

class MaterialCreateSchema(BaseModel):
    """
    Схема для создания материала.
    """
    type: str = Field(..., description="Тип материала")
    thickness: str = Field(..., description="Толщина материала")
    color: str = Field(..., description="Цвет материала")

class SheetsCreate(BaseModel):
    """
    Схема для создания информации о листах для задачи.
    """
    width: int = Field(..., description="Ширина листа")
    length: int = Field(..., description="Длина листа")
    quantity: int = Field(..., description="Количество листов")

class CommonProductFields(BaseModel):
    quantity: int = Field(..., description="Количество")
    color: str = Field(..., description="Цвет")
    painting: bool = Field(..., description="Покраска")

class CassetteProduct(CommonProductFields):
    cassette_type: str
    description: str

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
    panel_width: float
    groove: float
    length: float
    has_endcap: bool

class SheetProduct(CommonProductFields):
    pass

class ProductBase(BaseModel):
    product_type: ProductTypeEnum

class CassetteWrapper(ProductBase, CassetteProduct):
    product_type: Literal[ProductTypeEnum.CASSETTE]

class ProfileWrapper(ProductBase, ProfileProduct):
    product_type: Literal[ProductTypeEnum.PROFILE]

class KlamerWrapper(ProductBase, KlamerProduct):
    product_type: Literal[ProductTypeEnum.KLAMER]

class BracketWrapper(ProductBase, BracketProduct):
    product_type: Literal[ProductTypeEnum.BRACKET]

class ExtensionBracketWrapper(ProductBase, ExtensionBracketProduct):
    product_type: Literal[ProductTypeEnum.EXTENSION_BRACKET]

class LinearPanelWrapper(ProductBase, LinearPanelProduct):
    product_type: Literal[ProductTypeEnum.LINEAR_PANEL]

class SheetWrapper(ProductBase, SheetProduct):
    product_type: Literal[ProductTypeEnum.SHEET]

ProductDetail = Union[
    CassetteWrapper,
    ProfileWrapper,
    KlamerWrapper,
    BracketWrapper,
    ExtensionBracketWrapper,
    LinearPanelWrapper,
    SheetWrapper
]
class TaskCreate(BaseModel):
    """
    Схема для создания задачи в рамках заявки.
    """
    product_name: str = Field(..., description="имя продукта")
    product_details: list[ProductDetail] = Field(..., description="Детали продукта")
    material: MaterialCreateSchema = Field(..., description="материал")
    sheets: Optional[List[SheetsCreate]] = Field(None, description="Листы")
    urgency: UrgencyEnum = Field(..., description="Срочность")
    workshops: List[str] = Field(..., description="Рабочие места")
    employees: List[int] = Field(..., description="Сотрудники")

