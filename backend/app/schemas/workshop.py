from pydantic import BaseModel, ConfigDict, Field


class WorkshopBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Название цеха")


class WorkshopRead(WorkshopBase):
    id: int = Field(..., description="ID цеха")
