from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    APIRouter,
    Request
)
from fastapi.responses import JSONResponse
from dishka.integrations.fastapi import setup_dishka
from sqlalchemy.orm import (
    registry,
    relationship,
)
from nlp.errors import HandlingError
from nlp.container import container
from nlp.routes import *
from nlp.entities import *
from nlp.tables import *


def map_tables():
    reg = registry()
    reg.map_imperatively(Task, tasks)
    reg.map_imperatively(User, users)
    reg.map_imperatively(Project, projects, properties={
        "users": relationship(User, users_projects, lazy="raise"),
        "tasks": relationship(Task, lazy="selectin", cascade="all, delete-orphan")
    })


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_routers(app)
    map_tables()
    yield
    await container.close()

app = FastAPI(lifespan=lifespan)
setup_dishka(container, app)


@app.exception_handler(HandlingError)
async def handle_error(r: Request, err: HandlingError):
    return JSONResponse({"detail": str(err)}, err.status)


def setup_routers(app: FastAPI):
    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(task_router)
    api_router.include_router(user_router)
    api_router.include_router(project_router)
    app.include_router(api_router)
