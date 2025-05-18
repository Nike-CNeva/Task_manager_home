from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.app.models.enums import UserTypeEnum, WorkshopEnum



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

class UserCreate(UserBase):
    password: str = Field(..., description="Пароль пользователя")

class UserSaveForm(UserBase):
    id: int
    password: str = Field(..., description="Пароль пользователя")
    workshops: List[WorkshopEnum] = Field(..., description="Список цехов")


class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    

class UserWithWorkshops(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    name: str
    firstname: str
    username: str
    email: str
    telegram: str
    user_type: str
    workshops: List[str]