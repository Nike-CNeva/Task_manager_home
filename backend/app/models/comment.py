from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from backend.app.database.database import Base
from sqlalchemy.orm import relationship
from .association_table import *

# Comment Table
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    comment = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
    # One-to-Many связь с Task
    task = relationship("Task", back_populates="comments")
    # Many-to-Many связь с User
    users = relationship("User", secondary=comment_user_association, back_populates="comments")


