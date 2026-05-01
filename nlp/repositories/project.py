from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from nlp.entities import Project
from nlp.tables import users_projects
from .base import BaseAlchemyRepository


class ProjectRepository(BaseAlchemyRepository):
    async def get_user_projects(self, user_id: int) -> list[Project]:
        stmt = (
            select(Project)
            .join(users_projects, users_projects.c.project_id == Project.id)
            .where(users_projects.c.user_id == user_id)
        )
        res = await self.session.scalars(stmt)
        return res.all()

    async def get_by_id(self, project_id: int) -> Optional[Project]:
        return await self.session.scalar(
            select(Project).where(Project.id == project_id).options(selectinload(Project.id))
        )
