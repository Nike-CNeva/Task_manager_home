from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from backend.app.database.database import Base
from backend.app.models.enums import ManagerEnum
from sqlalchemy.orm import relationship

# Bid Table
class Bid(Base):
    __tablename__ = "bid"
    id = Column(Integer, primary_key=True, index=True)
    task_number = Column(String(50), nullable=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    manager = Column(Enum(ManagerEnum), nullable=False)
    files = relationship("Files", back_populates="bid", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="bid", cascade="all, delete-orphan")
    customer = relationship("Customer", back_populates="bid")

# Customer Table
class Customer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    bid = relationship("Bid", back_populates="customer")
