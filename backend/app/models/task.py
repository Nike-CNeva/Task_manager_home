from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String, Table
from sqlalchemy.orm import relationship
from backend.app.database.database import Base
from .enums import UrgencyEnum, StatusEnum
from sqlalchemy.sql import func
from .association_table import *

# Task Table
class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    bid_id = Column(Integer, ForeignKey("bid.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    material_id = Column(Integer, ForeignKey("material.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=True)
    urgency = Column(Enum(UrgencyEnum), nullable=False)
    status = Column(Enum(StatusEnum), default="NEW")
    waste = Column(String(50), nullable=True)
    weight = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    # One-to-Many связи
    sheets = relationship("Sheets", back_populates="task", cascade="all, delete-orphan")
    bid = relationship("Bid", back_populates="tasks")
    product = relationship("Product", back_populates="tasks", cascade="all, delete-orphan", single_parent=True)
    material = relationship("Material", back_populates="tasks", cascade="all, delete-orphan", single_parent=True)
    # One-to-Many связь с Comment
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    workshops = relationship("TaskWorkshop", back_populates="task", cascade="all, delete-orphan")
    # Many-to-Many связи
    responsible_users = relationship("User", secondary=task_responsible_association, back_populates="tasks")

# TaskWorkshop Table
class TaskWorkshop(Base):
    __tablename__ = "task_workshops"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id", ondelete="CASCADE"))
    workshop_id = Column(Integer, ForeignKey("workshop.id", ondelete="CASCADE"))
    status = Column(Enum(StatusEnum), default="ON_HOLD")  # Статус выполнения в цехе
    task = relationship("Task", back_populates="workshops")
    workshop = relationship("Workshop", back_populates="task_workshops")
