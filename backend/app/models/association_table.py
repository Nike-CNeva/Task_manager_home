from sqlalchemy import Column, ForeignKey, Integer, Table
from backend.app.database.database import Base


user_workshop_association = Table(
    "user_workshop_association",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("workshop_id", Integer, ForeignKey("workshop.id"), primary_key=True)
)

task_responsible_association = Table(
    "task_responsible_association",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("task.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)