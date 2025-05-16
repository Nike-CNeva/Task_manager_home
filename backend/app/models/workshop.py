from sqlalchemy import Enum as SQLEnum
from backend.app.database.database import Base
from backend.app.models.enums import WorkshopEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.models.association_table import *

class Workshop(Base):
    __tablename__ = "workshop"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[WorkshopEnum] = mapped_column(SQLEnum(WorkshopEnum), nullable=False)
    # Связь Many-to-Many с Task
    task_workshops = relationship("TaskWorkshop", back_populates="workshop", cascade="all, delete-orphan")
    users = relationship("User", secondary=user_workshop_association, back_populates="workshops")
  