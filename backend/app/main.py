from uuid import UUID

from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

from backend.app.domain.task import Task
app = FastAPI()

tasks: dict[UUID,Task] = {}

class TaskRecived(BaseModel):
    description: str

@app.get("/")
def root():
    return {"message": "Hello, from DevTeam-AI!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/task")
def create_task(task: TaskRecived):
    new_task = Task(description=task.description)
    tasks[new_task.id] = new_task
    return {
        "id": str(new_task.id),
        "description": new_task.description,
        "status": new_task.status.value
    }

@app.get("/task/{task_id}")
def get_task(task_id: UUID):
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "id": str(task.id),
        "description": task.description,
        "status": task.status.value
    }