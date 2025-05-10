from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import ProductTypeEnum, StatusEnum, UserTypeEnum, WorkshopEnum


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    name: str = Field(..., description="Имя пользователя")
    firstname: Optional[str] = Field(None, description="Фамилия пользователя")
    email: Optional[EmailStr] = Field(None, description="Email пользователя")
    telegram: Optional[str] = Field(None, description="Telegram пользователя")
    username: str = Field(..., description="Имя пользователя для входа")
    user_type: UserTypeEnum = Field(..., description="Тип пользователя")
    is_active: Optional[bool] = Field(True, description="Активен ли пользователь")

    
class UserRead(UserBase):
    id: int = Field(..., description="ID пользователя")


class UserSaveForm(UserBase):
    password: Optional[str] = Field(None, description="Пароль пользователя")
    workshops: List[WorkshopEnum] = Field(..., description="Список цехов")


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

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


class BidBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_number: Optional[str] = Field(None, description="Номер заявки")
    manager: str = Field(..., description="Менеджер")


class BidRead(BidBase):
    id: int = Field(..., description="ID заявки")


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str = Field(..., description="Тип продукта")


class ProductRead(ProductBase):
    id: int = Field(..., description="ID продукта")

class ProductResponse(BaseModel):
    id: int = Field(..., description="ID продукта")
    type: ProductTypeEnum = Field(..., description="Тип продукта")
    
class MaterialBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    form: str = Field(..., description="Форма материала")
    type: str = Field(..., description="Тип материала")
    thickness: str = Field(..., description="Толщина материала")
    painting: bool = Field(False, description="Наличие покраски")


class MaterialRead(MaterialBase):
    id: int = Field(..., description="ID материала")


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Имя заказчика")


class CustomerRead(CustomerBase):
    id: int = Field(..., description="ID заказчика")


class WorkshopBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Название цеха")


class WorkshopRead(WorkshopBase):
    id: int = Field(..., description="ID цеха")


class CommentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    comment: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")
    is_read: bool = Field(False, description="Прочитан ли комментарий")
    is_deleted: bool = Field(False, description="Удален ли комментарий")


class CommentRead(CommentBase):
    id: int = Field(..., description="ID комментария")


class UserWithTasks(UserRead):
    tasks: List[TaskRead] = Field(default_factory=list, description="Список задач пользователя")


class TaskWithUsers(TaskRead):
    responsible_users: List[UserRead] = Field(default_factory=list, description="Список ответственных пользователей")


class BidWithTasks(BidRead):
    tasks: List[TaskRead] = Field(default_factory=list, description="Список задач в заявке")


class CustomerWithBids(CustomerRead):
    bid: List[BidRead] = Field(default_factory=list, description="Список заявок заказчика")


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


class BidCreateRequest(BaseModel):
    """
    Схема для создания заявки.
    """
    customer_id: int = Field(..., description="ID заказчика")
    manager: str = Field(..., description="Менеджер")
    status: str = Field(..., description="Статус")
    comment: Optional[str] = Field(None, description="Комментарий к заявке")
    tasks: List[TaskCreateRequest] = Field(..., description="Список задач")


class CustomerCreateRequest(BaseModel):
    """
    Схема для создания заказчика.
    """
    name: str = Field(..., description="Имя заказчика")

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str