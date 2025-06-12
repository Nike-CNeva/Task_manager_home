from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, String
from backend.app.database.database import Base
from backend.app.models.enums import ProductTypeEnum, ProfileTypeEnum, KlamerTypeEnum, CassetteTypeEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Product Table
class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[ProductTypeEnum] = mapped_column(SQLEnum(ProductTypeEnum), nullable=False)

    task_products = relationship("TaskProduct", back_populates="product", cascade="all, delete-orphan", uselist=False)
    profile = relationship("Profile", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    klamer = relationship("Klamer", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    bracket = relationship("Bracket", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    extension_bracket = relationship("ExtensionBracket", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    cassette = relationship("Cassette", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    linear_panel = relationship("LinearPanel", back_populates="product", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    
# Profile Table
class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    profile_type: Mapped[ProfileTypeEnum] = mapped_column(SQLEnum(ProfileTypeEnum), nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    product = relationship("Product", back_populates="profile")

# Klamer Table
class Klamer(Base):
    __tablename__ = "klamer"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    klamer_type: Mapped[KlamerTypeEnum] = mapped_column(SQLEnum(KlamerTypeEnum), nullable=False)
    product = relationship("Product", back_populates="klamer")

# Bracket Table
class Bracket(Base):
    __tablename__ = "bracket"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[str] = mapped_column(nullable=False)
    product = relationship("Product", back_populates="bracket")

# Extension Bracket Table
class ExtensionBracket(Base):
    __tablename__ = "extension_bracket"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[str] = mapped_column(nullable=False)
    heel: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    product = relationship("Product", back_populates="extension_bracket")

# Cassette Table
class Cassette(Base):
    __tablename__ = "cassette"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    cassette_type: Mapped[CassetteTypeEnum] = mapped_column(SQLEnum(CassetteTypeEnum), nullable=False)
    product = relationship("Product", back_populates="cassette")

# Linear Panel Table
class LinearPanel(Base):
    __tablename__ = "linear_panel"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id", ondelete="CASCADE"),  nullable=False)
    field: Mapped[int] = mapped_column(nullable=False)
    rust: Mapped[int] = mapped_column(nullable=False)
    length: Mapped[int] = mapped_column(nullable=False)
    butt_end: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    product = relationship("Product", back_populates="linear_panel")
