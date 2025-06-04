from sqlalchemy import ForeignKey, String
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
