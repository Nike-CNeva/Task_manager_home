from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from backend.app.database.database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Comment Table
class Comment(Base):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    # One-to-Many связь с Task
    task = relationship("Task", back_populates="comments")
    # Many-to-Many связь с User
    user = relationship("User", back_populates="comments")


