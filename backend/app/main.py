
from fastapi import FastAPI, HTTPException
from uuid import UUID
from backend.app.api import CreateTaskRequest, TaskResponse

from backend.app.application.task_service import TaskService
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.repositories.task_run_repository import TaskRunRepository

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
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)
        task = service.create_task(request.description)
        return TaskResponse(
            id=task.id,
            description=task.description,
            status=task.status
        )

@app.post("/tasks/{task_id}/runs")
def start_task_run(task_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        try:
            task_run = service.start_task_run(task_id)
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return {
            "id": task_run.id,
            "task_id": task_run.task_id,
            "attempt": task_run.attempt,
            "status": task_run.status,
            "created_at": task_run.created_at,
            "started_at": task_run.started_at,
        }

@app.post("/task-runs/{run_id}/complete")
def complete_task_run(run_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        try:
            task_run = service.complete_task_run(run_id)
        except ValueError as error:
            raise HTTPException(
                status_code=404,
                detail=str(error),
            )

        return {
            "id": task_run.id,
            "task_id": task_run.task_id,
            "attempt": task_run.attempt,
            "status": task_run.status,
            "created_at": task_run.created_at,
            "started_at": task_run.started_at,
            "finished_at": task_run.finished_at,
            "error": task_run.error,
        }

@app.post("/task-runs/{run_id}/fail")
def fail_task_run(run_id: UUID, error: str):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        try:
            task_run = service.fail_task_run(run_id, error)
        except ValueError as exception:
            raise HTTPException(
                status_code=404,
                detail=str(exception),
            )

        return {
            "id": task_run.id,
            "task_id": task_run.task_id,
            "attempt": task_run.attempt,
            "status": task_run.status,
            "created_at": task_run.created_at,
            "started_at": task_run.started_at,
            "finished_at": task_run.finished_at,
            "error": task_run.error,
        }
    
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        task = service.get_task(task_id)

        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=task.id,
            description=task.description,
            status=task.status,
        )

@app.get("/task-runs/{run_id}")
def get_task_run(run_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        task_run = service.get_task_run(run_id)

        if task_run is None:
            raise HTTPException(
                status_code=404,
                detail="TaskRun not found",
            )

        return {
            "id": task_run.id,
            "task_id": task_run.task_id,
            "attempt": task_run.attempt,
            "status": task_run.status,
            "created_at": task_run.created_at,
            "started_at": task_run.started_at,
            "finished_at": task_run.finished_at,
            "error": task_run.error,
        }

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        tasks = service.list_tasks()

        return [
            TaskResponse(
                id=task.id,
                description=task.description,
                status=task.status,
            )
            for task in tasks
        ]

@app.get("/tasks/{task_id}/runs")
def list_task_runs(task_id: UUID):
    with SessionLocal() as session:
        repository = TaskRepository(session)
        task_run_repository = TaskRunRepository(session)
        service = TaskService(repository, task_run_repository)

        task = service.get_task(task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        runs = service.list_task_runs(task_id)

        return [
            {
                "id": run.id,
                "task_id": run.task_id,
                "attempt": run.attempt,
                "status": run.status,
                "created_at": run.created_at,
                "started_at": run.started_at,
                "finished_at": run.finished_at,
                "error": run.error,
            }
            for run in runs
        ]