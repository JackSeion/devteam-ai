from uuid import uuid4

from backend.app.domain.task_run import TaskRun
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.repositories.task_run_repository import TaskRunRepository
from backend.app.domain.task import Task


with SessionLocal() as session:
    task_repository = TaskRepository(session)
    task_run_repository = TaskRunRepository(session)

    task = Task("TaskRun repository test")
    task_repository.create(task)

    task_run = TaskRun(
        task_id=task.id,
        attempt=1,
    )

    task_run_repository.create(task_run)

    print("Created:", task_run.id)

    fetched = task_run_repository.get_by_id(task_run.id)

    print("Fetched:", fetched.id)
    print("Task ID:", fetched.task_id)
    print("Attempt:", fetched.attempt)
    print("Status:", fetched.status)

    runs = task_run_repository.list_by_task(task.id)

    print("Runs for task:", len(runs))

    task_run.start()
    updated = task_run_repository.update(task_run)

    print("Updated status:", updated.status)

    fetched_updated = task_run_repository.get_by_id(task_run.id)

    print("Fetched updated status:", fetched_updated.status)
    print("Started at:", fetched_updated.started_at)