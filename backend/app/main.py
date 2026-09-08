
from fastapi import FastAPI, HTTPException
from uuid import UUID
from backend.app.api import CreateTaskRequest, TaskResponse

from backend.app.application.task_service import TaskService
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.database import SessionLocal

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello, from DevTeam-AI!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(request: CreateTaskRequest):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        service = TaskService(repository)
        task = service.create_task(request.description)
        return TaskResponse(
            id=task.id,
            description=task.description,
            status=task.status
        )
    
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        service = TaskService(repository)

        task = service.get_task(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=task.id,
            description=task.description,
            status=task.status,
        )

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    with SessionLocal() as session:
        repository = TaskRepository(session)
        service = TaskService(repository)

        tasks = service.list_tasks()

        return [
            TaskResponse(
                id=task.id,
                description=task.description,
                status=task.status,
            )
            for task in tasks
        ]