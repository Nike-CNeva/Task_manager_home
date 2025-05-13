from sqlalchemy import Column, Enum, Integer
from backend.app.database.database import Base
from backend.app.models.enums import WorkshopEnum
from sqlalchemy.orm import relationship
from .association_table import *

class Workshop(Base):
    __tablename__ = "workshop"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(WorkshopEnum), nullable=False)
    # Связь Many-to-Many с Task
    task_workshops = relationship("TaskWorkshop", back_populates="workshop", cascade="all, delete-orphan")
    users = relationship("User", secondary=user_workshop_association, back_populates="workshops")
  