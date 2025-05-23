from typing import List, Optional
from pydantic import BaseModel


# 👤 Клиенты, статусы, менеджеры и т.п.
class ReferenceOption(BaseModel):
    value: str
    name: str


# 🧩 Поля продуктов (input формы)
class ProductField(BaseModel):
    name: str
    label: str
    type: str  # select, number, text, checkbox
    options: Optional[List[ReferenceOption]] = None  # только для select


# 📦 Продукты с полями
class ProductReference(BaseModel):
    value: str
    name: str
    fields: List[ProductField]

class MaterialField(BaseModel):
    name: str
    label: str
    type: str
    options: Optional[List[ReferenceOption]] = None


class EmployeeReference(BaseModel):
    id: int
    name: str
    firstname: str

class CustomerReference(BaseModel):
    id: int
    name: str

# 📋 Финальный ответ
class ReferenceDataResponse(BaseModel):
    customers: List[CustomerReference]
    managers: List[ReferenceOption]
    urgency: List[ReferenceOption]
    products: List[ProductReference]
    materials: List[MaterialField]
    workshops: List[ReferenceOption]
    employees: List[EmployeeReference]
