from fastapi import APIRouter
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)

from nlp.entities import Project
from nlp.repositories import (
    UserRepository,
    ProjectRepository
)
from nlp.types import AuthenticatedUserId
from .dtos.project import (
    CreateProjectDTO,
    ShowProjectDTO
)

project_router = APIRouter(prefix="/projects", tags=["Projects router"], route_class=DishkaRoute)


@project_router.post("")
async def create_project(
        dto: CreateProjectDTO,
        user_id: FromDishka[AuthenticatedUserId],
        user_repo: FromDishka[UserRepository]
) -> ShowProjectDTO:
    user = await user_repo.get_by_id(user_id),
    project: Project(dto.name, dto.description)
    project.users.append(user)
    user_repo.session.add(project)
    await user_repo.session.flush([project])
    return project


@project_router.get("")
async def get_user_projects(
        user_id: FromDishka[AuthenticatedUserId],
        project_repo: FromDishka[ProjectRepository]
) -> list[ShowProjectDTO]:
    return await project_repo.get_user_projects(user_id)
