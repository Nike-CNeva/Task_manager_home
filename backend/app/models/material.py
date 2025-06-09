# Materials Tables
from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.app.models.enums import MaterialTypeEnum, MaterialThicknessEnum

class Material(Base):
    __tablename__ = "material"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[MaterialTypeEnum] = mapped_column(SQLEnum(MaterialTypeEnum), nullable=False)
    thickness: Mapped[MaterialThicknessEnum] = mapped_column(SQLEnum(MaterialThicknessEnum), nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=True)
    waste: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[int] = mapped_column(ForeignKey("waight.id", ondelete="CASCADE"), nullable=True)
    tasks = relationship("Task", back_populates="material", uselist=False)
    weight = relationship("Waight", back_populates="material", cascade="all, delete-orphan", passive_deletes=True)


# Additional Tables
class Sheets(Base):
    __tablename__ = "sheets"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id", ondelete="CASCADE"), nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    # Обратная связь One-to-Many
    task = relationship("Task", back_populates="sheets")

class Weight(Base):
    __tablename__ = "weight"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    weight: Mapped[float] = mapped_column(nullable=False)
    from_waste: Mapped[bool] = mapped_column(Boolean, default=False)
    material = relationship("Material", back_populates="weight")