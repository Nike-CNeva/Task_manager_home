from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from backend.app.models.enums import UserTypeEnum, WorkshopEnum
from backend.app.schemas.workshop import WorkshopRead



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
    id: Optional[int] = Field(None, description="ID пользователя")
    workshops: List[WorkshopEnum] = Field(default_factory=list, description="Список цехов")
    password: Optional[str] = Field(None, description="Пароль (только при создании)")

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str
    

class UserWithWorkshops(UserRead):
    workshops: List[WorkshopRead]


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    name: str
    firstname: Optional[str]