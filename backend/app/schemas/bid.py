from typing import List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, model_validator
from backend.app.models.enums import ManagerEnum
from backend.app.schemas.task import TaskCreate, TaskRead


class BidBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_number: Optional[str] = Field(None, description="Номер заявки")
    manager: str = Field(..., description="Менеджер")


class BidRead(BidBase):
    id: int = Field(..., description="ID заявки")


class BidWithTasks(BidRead):
    tasks: List[TaskRead] = Field(default_factory=list, description="Список задач в заявке")

class BidCreate(BaseModel):
    """
    Схема для создания заявки.
    """
    task_number: Optional[int] = Field(None, description="Номер заявки")
    customer: Union[int, Literal["new"]] = Field(..., description="ID заказчика или 'new'")
    new_customer: str | None = Field(default=None, description="Название нового заказчика")
    manager: ManagerEnum = Field(..., description="Менеджер")
    comment: Optional[str] = Field(None, description="Комментарий к заявке")
    products: List[TaskCreate] = Field(..., description="Список задач")


    @model_validator(mode="after")
    def check_customer_fields(self) -> 'BidCreate':
        if self.customer == "new":
            if not self.new_customer:
                raise ValueError("Поле 'newcustomer' обязательно, если customer == 'new'")
        else:
            if self.new_customer:
                raise ValueError("Поле 'newcustomer' должно быть пустым, если указан существующий customer")
        return self