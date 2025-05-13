from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship
from .enums import ProductTypeEnum, ProfileTypeEnum, KlamerTypeEnum, CassetteTypeEnum

# Product Table
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(ProductTypeEnum), nullable=False)
    tasks = relationship("Task", back_populates="product", uselist=False)
    profile = relationship("Profile", back_populates="product", cascade="all, delete-orphan")
    klamer = relationship("Klamer", back_populates="product", cascade="all, delete-orphan")
    bracket = relationship("Bracket", back_populates="product", cascade="all, delete-orphan")
    extension_bracket = relationship("ExtensionBracket", back_populates="product", cascade="all, delete-orphan")
    cassette = relationship("Cassette", back_populates="product", cascade="all, delete-orphan")
    linear_panel = relationship("LinearPanel", back_populates="product", cascade="all, delete-orphan")

# Profile Table
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    profile_type = Column(Enum(ProfileTypeEnum), nullable=False)
    length = Column(Integer, nullable=False)
    product = relationship("Product", back_populates="profile")

# Klamer Table
class Klamer(Base):
    __tablename__ = "klamer"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    type = Column(Enum(KlamerTypeEnum), nullable=False)
    product = relationship("Product", back_populates="klamer")

# Bracket Table
class Bracket(Base):
    __tablename__ = "bracket"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    width = Column(Integer, nullable=False)
    length = Column(String(50), nullable=False)
    thickness = Column(Integer, nullable=False)
    product = relationship("Product", back_populates="bracket")

# Extension Bracket Table
class ExtensionBracket(Base):
    __tablename__ = "extension_bracket"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    width = Column(Integer, nullable=False)
    length = Column(String(50), nullable=False)
    heel = Column(Boolean, default=True)
    product = relationship("Product", back_populates="extension_bracket")

# Cassette Table
class Cassette(Base):
    __tablename__ = "cassette"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    cassette_type = Column(Enum(CassetteTypeEnum), nullable=False)
    description = Column(String(255), nullable=True)
    product = relationship("Product", back_populates="cassette")

# Linear Panel Table
class LinearPanel(Base):
    __tablename__ = "linear_panel"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    field = Column(Integer, nullable=False)
    rust = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    butt_end = Column(Boolean, nullable=False, default=False)
    product = relationship("Product", back_populates="linear_panel")
