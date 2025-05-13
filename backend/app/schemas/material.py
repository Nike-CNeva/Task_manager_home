from pydantic import BaseModel, ConfigDict, Field


class MaterialBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    form: str = Field(..., description="Форма материала")
    type: str = Field(..., description="Тип материала")
    thickness: str = Field(..., description="Толщина материала")
    painting: bool = Field(False, description="Наличие покраски")


class MaterialRead(MaterialBase):
    id: int = Field(..., description="ID материала")
