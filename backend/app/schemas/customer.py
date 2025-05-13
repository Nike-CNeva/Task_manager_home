from typing import List
from pydantic import BaseModel, ConfigDict, Field

from backend.app.schemas.bid import BidRead


class CustomerBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Имя заказчика")


class CustomerRead(CustomerBase):
    id: int = Field(..., description="ID заказчика")

class CustomerWithBids(CustomerRead):
    bid: List[BidRead] = Field(default_factory=list, description="Список заявок заказчика")


class CustomerCreateRequest(BaseModel):
    """
    Схема для создания заказчика.
    """
    name: str = Field(..., description="Имя заказчика")
