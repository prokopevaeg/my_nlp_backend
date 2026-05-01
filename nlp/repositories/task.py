from typing import Optional

from sqlalchemy import select

from nlp.entities import (
    Task,
    TaskStatus
)
from .base import BaseAlchemyRepository


class TaskRepository(BaseAlchemyRepository):
    async def get_by_id(self, task_id: int) -> Optional[Task]:
        return await self.session.scalar(select(Task).where(Task.id == task_id))

    async def get_user_project_tasks(self, user_id: int, project_id: int, status: TaskStatus) -> list[Task]:
        stmt = (
            select(Task).where(Task.user_id == user_id, Task.project_id == project_id, Task.status == status)
        )
        return await self.session.scalars(stmt)
