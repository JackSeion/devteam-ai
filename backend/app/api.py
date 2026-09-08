from uuid import UUID

from pydantic import BaseModel

from backend.app.domain.task import TaskStatus


class CreateTaskRequest(BaseModel):
    description: str


class TaskResponse(BaseModel):
    id: UUID
    description: str
    status: TaskStatus