from sqlalchemy import ForeignKey, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.database.database import Base
from .enums import UrgencyEnum, StatusEnum
from sqlalchemy.sql import func
from .association_table import *

# Task Table
class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("material.id", ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=True)
    urgency: Mapped[UrgencyEnum] = mapped_column(SQLEnum(UrgencyEnum), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SQLEnum(StatusEnum), default="NEW")
    waste: Mapped[str] = mapped_column(String(50), nullable=True)
    weight: Mapped[str] = mapped_column(String(50), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
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
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    workshop_id: Mapped[int] = mapped_column(ForeignKey("workshop.id", ondelete="CASCADE"))
    status: Mapped[StatusEnum] = mapped_column(SQLEnum(StatusEnum), default="ON_HOLD")
    task = relationship("Task", back_populates="workshops")
    workshop = relationship("Workshop", back_populates="task_workshops")
