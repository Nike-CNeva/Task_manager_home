from sqlalchemy import Enum as SQLEnum, String, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.database.database import Base
from backend.app.models.enums import UserTypeEnum
from backend.app.models.association_table import *


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True, unique=True)
    telegram: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    user_type: Mapped[UserTypeEnum] = mapped_column(SQLEnum(UserTypeEnum), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Связь Many-to-Many с Task (Ответственные)
    tasks = relationship("Task", secondary=task_responsible_association, back_populates="responsible_users", lazy="selectin")
    workshops = relationship("Workshop", secondary=user_workshop_association, back_populates="users")
    comments = relationship("Comment", back_populates="user")
