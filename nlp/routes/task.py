import asyncio
import random

from fastapi import (
    APIRouter,
    Query
)
from dishka.integrations.fastapi import (
    FromDishka,
    DishkaRoute
)

from .dtos.task import (
    CreateTaskDTO,
    ShowTaskDTO
)
from nlp.types import AuthenticatedUserId
from nlp.entities import (
    TaskStatus,
    Task

)
from nlp.repositories import (
    ProjectRepository,
    UserRepository,
    TaskRepository
)
from nlp.errors import (
    UndefinedProjectError,
    UserDoesNotRelatedToProject
)

task_router = APIRouter(prefix="/tasks", tags=["Tasks router"], route_class=DishkaRoute)


@task_router.post("")
async def create_task(
    dto: CreateTaskDTO,
    user_id: FromDishka[AuthenticatedUserId],
    project_repo: FromDishka[ProjectRepository],
    user_repo: FromDishka[UserRepository]
) -> ShowTaskDTO:
    project = await project_repo.get_by_id(dto.project_id)
    if not project:
        raise UndefinedProjectError("Project does not exist")
    user = await user_repo.get_by_id(user_id)
    if not user in project.users:
        raise UserDoesNotRelatedProject("Current user not in the project", status=403)
    task = Task(dto.name, user_id, project.id, dto.data)
    project_repo.session.add(task)
    await project_repo.session.flush([task])
    await asyncio.sleep(random.randint(1, 3))
    task.finish(random.choice([TaskStatus.CRASHED, TaskStatus.DONE]))
    return task


@task_router.get("/project/{project_id}")
async def get_user_project_tasks(
    project_id: int,
    user_id: FromDishka[AuthenticatedUserId],
    task_repo: FromDishka[TaskRepository],
    status: TaskStatus = Query()
) -> list[ShowTaskDTO]:
    return await task_repo.get_user_project_tasks(user_id, project_id, status)

