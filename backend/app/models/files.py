from sqlalchemy import Column, ForeignKey, Integer, String
from backend.app.database.database import Base
from sqlalchemy.orm import relationship

class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    bid_id = Column(Integer, ForeignKey("bid.id"), nullable=False)  # Привязываем к Task
    file_name = Column(String(255), nullable=False)
    file_path = Column(String, nullable=False)
    # Обратная связь One-to-Many
    bid = relationship("Bid", back_populates="files")
