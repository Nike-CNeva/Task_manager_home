from sqlalchemy import Boolean, ForeignKey, DateTime, Enum as SQLEnum, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.database.database import Base
from backend.app.models.enums import UrgencyEnum, StatusEnum
from sqlalchemy.sql import func
from backend.app.models.association_table import *
from sqlalchemy.ext.asyncio import AsyncSession
# Task Table
class Task(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id"), nullable=False)
    material_id: Mapped[int] = mapped_column(ForeignKey("material.id", ondelete="CASCADE"), nullable=False)
    urgency: Mapped[UrgencyEnum] = mapped_column(SQLEnum(UrgencyEnum), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(SQLEnum(StatusEnum), default="NEW")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    sheets = relationship("Sheets", back_populates="task", cascade="all, delete-orphan")
    bid = relationship("Bid", back_populates="tasks")
    material = relationship("Material", back_populates="tasks")
    task_products = relationship("TaskProduct", back_populates="task", cascade="all, delete-orphan", single_parent=True)
    workshops = relationship("TaskWorkshop", back_populates="task", cascade="all, delete-orphan")
    responsible_users = relationship("User", secondary=task_responsible_association, back_populates="tasks", cascade="all, delete")

    @property
    def total_quantity(self):
        return sum(tp.quantity for tp in self.task_products)
    
    @property
    def done_quantity(self):
        return sum(tp.done_quantity for tp in self.task_products)
    
    @property
    def progress_percent(self):
        total = self.total_quantity
        done = self.done_quantity
        return (done / total * 100) if total else 0
    
    async def get_progress_percent(self, session: AsyncSession) -> float:
        # Асинхронно обновить/подгрузить task_products
        await session.refresh(self, ['task_products'])
        total = sum(tp.quantity for tp in self.task_products)
        done = sum(tp.done_quantity for tp in self.task_products)
        return (done / total * 100) if total else 0
    
# TaskWorkshop Table
class TaskWorkshop(Base):
    __tablename__ = "task_workshops"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    workshop_id: Mapped[int] = mapped_column(ForeignKey("workshop.id", ondelete="CASCADE"))
    status: Mapped[StatusEnum] = mapped_column(SQLEnum(StatusEnum), default="NEW")
    progress_percent: Mapped[float] = mapped_column(default=0.0)
    task = relationship("Task", back_populates="workshops")
    workshop = relationship("Workshop", back_populates="task_workshops")

class TaskProduct(Base):
    __tablename__ = "task_products"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    color: Mapped[str] = mapped_column(String(50), nullable=True)
    painting: Mapped[bool] = mapped_column(Boolean, default=False)
    quantity: Mapped[int]
    done_quantity: Mapped[int] = mapped_column(default=0)

    task = relationship("Task", back_populates="task_products")
    product = relationship("Product", back_populates="task_products", cascade="all, delete-orphan")