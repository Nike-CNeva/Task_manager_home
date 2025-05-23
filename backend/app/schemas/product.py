from cProfile import label
from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import ProductTypeEnum


class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str = Field(..., description="Тип продукта")


class ProductRead(ProductBase):
    id: int = Field(..., description="ID продукта")

class ProductResponse(BaseModel):
    value: int = Field(..., description="ID продукта")
    label: ProductTypeEnum = Field(..., description="Тип продукта")
 