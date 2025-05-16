from typing import List
from pydantic import Field

from backend.app.schemas.task import TaskRead
from backend.app.schemas.user import UserRead


class TaskWithUsers(TaskRead):
    responsible_users: List[UserRead] = Field(default_factory=list, description="Список ответственных пользователей")

class UserWithTasks(UserRead):
    tasks: List[TaskRead] = Field(default_factory=list, description="Список задач пользователя")
