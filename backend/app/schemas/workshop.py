from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.enums import WorkshopEnum


class WorkshopBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    name: WorkshopEnum = Field(..., description="Название цеха")


class WorkshopRead(WorkshopBase):
    id: int = Field(..., description="ID цеха")
