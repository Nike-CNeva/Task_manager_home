from sqlalchemy import Column, Enum, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from backend.app.database.database import Base
from .enums import UserTypeEnum
from .association_table import *


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True, unique=True)
    telegram = Column(String(50), nullable=True, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(60), nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    # Связь Many-to-Many с Task (Ответственные)
    tasks = relationship("Task", secondary=task_responsible_association, back_populates="responsible_users")
    workshops = relationship("Workshop", secondary=user_workshop_association, back_populates="users")
    comments = relationship("Comment", secondary=comment_user_association, back_populates="users")
