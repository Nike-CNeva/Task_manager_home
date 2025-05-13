# Materials Tables
from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .enums import MaterialFormEnum, MaterialTypeEnum, MaterialThicknessEnum

class Material(Base):
    __tablename__ = "material"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    form: Mapped[MaterialFormEnum] = mapped_column(SQLEnum(MaterialFormEnum), nullable=False)
    type: Mapped[MaterialTypeEnum] = mapped_column(SQLEnum(MaterialTypeEnum), nullable=False)
    thickness: Mapped[MaterialThicknessEnum] = mapped_column(SQLEnum(MaterialThicknessEnum), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=True)
    painting: Mapped[Boolean] = mapped_column(Boolean, default=False)
    tasks = relationship("Task", back_populates="material")

# Additional Tables
class Sheets(Base):
    __tablename__ = "sheets"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    # Обратная связь One-to-Many
    task = relationship("Task", back_populates="sheets")