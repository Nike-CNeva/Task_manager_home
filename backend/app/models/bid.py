from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from backend.app.database.database import Base
from backend.app.models.enums import ManagerEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Bid Table
class Bid(Base):
    __tablename__ = "bid"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_number: Mapped[int] = mapped_column(nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    manager: Mapped[ManagerEnum] = mapped_column(SQLEnum(ManagerEnum), nullable=False)
    files = relationship("Files", back_populates="bid", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="bid", cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="bid")
    comments = relationship("Comment", back_populates="bid", cascade="all, delete-orphan")
# Customer Table
class Customer(Base):
    __tablename__ = "customer"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    bid = relationship("Bid", back_populates="customer")
