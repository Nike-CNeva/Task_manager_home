from sqlalchemy import Boolean, ForeignKey, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Files(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bid_id: Mapped[int] = mapped_column(ForeignKey("bid.id", ondelete="CASCADE"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String(255), nullable=False)
    # Обратная связь One-to-Many
    bid = relationship("Bid", back_populates="files")
    # Один к одному с NestFile
    nest_file = relationship("NestFile", back_populates="file", uselist=False, cascade="all, delete")

class NestFile(Base):
    __tablename__ = "nest_file"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    nest_id: Mapped[int] = mapped_column(nullable=False)
    material: Mapped[str] = mapped_column(String(50), nullable=False)
    thickness: Mapped[str] = mapped_column(String(50), nullable=False)
    nc_file_name: Mapped[str] = mapped_column(String(50), nullable=False)
    sheet_utilization: Mapped[float] = mapped_column(nullable=False)
    sheet_size: Mapped[str] = mapped_column(String(50), nullable=False)
    time_per_sheet: Mapped[str] = mapped_column(String(50), nullable=False)
    nest_notes: Mapped[str] = mapped_column(String(255), nullable=True)
    sheet_quantity: Mapped[int] = mapped_column(nullable=False)
    sheet_quantity_done: Mapped[int] = mapped_column(nullable=True)
    nest_screen_file_path: Mapped[str] = mapped_column(String(255), nullable=False)

    # Связь с Files
    file = relationship("Files", back_populates="nest_file")

    # Один к одному с ClampLocations
    clamp_location = relationship("ClampLocations", back_populates="nest_file", uselist=False, cascade="all, delete")

    # Один ко многим с Parts и Tools
    parts = relationship("Parts", back_populates="nest_file", cascade="all, delete-orphan")
    tools = relationship("Tools", back_populates="nest_file", cascade="all, delete-orphan")

class ClampLocations(Base):
    __tablename__ = "clamp_locations"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nest_file_id: Mapped[int] = mapped_column(ForeignKey("nest_file.id", ondelete="CASCADE"), nullable=False)
    clamp_1: Mapped[int] = mapped_column(nullable=False)
    clamp_2: Mapped[int] = mapped_column(nullable=False)
    clamp_3: Mapped[int] = mapped_column(nullable=False)

    # Обратная связь
    nest_file = relationship("NestFile", back_populates="clamp_location")

class Parts(Base):
    __tablename__ = "parts"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nest_file_id: Mapped[int] = mapped_column(ForeignKey("nest_file.id", ondelete="CASCADE"), nullable=False)
    part_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    time_per_part: Mapped[str] = mapped_column(String(50), nullable=False)

    # Обратная связь
    nest_file = relationship("NestFile", back_populates="parts")

class Tools(Base):
    __tablename__ = "tools"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nest_file_id: Mapped[int] = mapped_column(ForeignKey("nest_file.id", ondelete="CASCADE"), nullable=False)
    station: Mapped[str] = mapped_column(String(50), nullable=False)
    tool: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[str] = mapped_column(String(50), nullable=False)
    angle: Mapped[int] = mapped_column(nullable=False)
    die: Mapped[float] = mapped_column(nullable=False)
    hits: Mapped[int] = mapped_column(nullable=False)

    # Обратная связь
    nest_file = relationship("NestFile", back_populates="tools")