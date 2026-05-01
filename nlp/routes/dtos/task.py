from datetime import datetime

from pydantic import BaseModel

from nlp.entities import TaskStatus


class CreateTaskDTO(BaseModel):
    name: str
    project_id: int
    data: str


class ShowTaskDTO(BaseModel):
    id: int
    name: str
    data: str
    project_id: int
    created_at: datetime
    updated_at: datetime
    status: TaskStatus
