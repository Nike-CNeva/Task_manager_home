# Materials Tables
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship
from .enums import MaterialFormEnum, MaterialTypeEnum, MaterialThicknessEnum

class Material(Base):
    __tablename__ = "material"
    id = Column(Integer, primary_key=True, index=True)
    form = Column(Enum(MaterialFormEnum), nullable=False)
    type = Column(Enum(MaterialTypeEnum), nullable=False)
    thickness = Column(Enum(MaterialThicknessEnum), nullable=False)
    color = Column(String(50), nullable=True)
    painting = Column(Boolean, default=False)
    tasks = relationship("Task", back_populates="material")

# Additional Tables
class Sheets(Base):
    __tablename__ = "sheets"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)  # Привязываем к Task
    width = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False )
    quantity = Column(Integer, nullable=False)
    # Обратная связь One-to-Many
    task = relationship("Task", back_populates="sheets")