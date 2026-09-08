from backend.app.domain.task import Task, TaskStatus
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.repositories.task_repository import TaskRepository


with SessionLocal() as session:
    repository = TaskRepository(session)

    task = Task("Repository CRUD test")
    repository.create(task)

    print("Created:", task.id)

    fetched = repository.get_by_id(task.id)
    print("Fetched:", fetched.description)

    fetched.status = TaskStatus.QUEUED
    fetched.description = "Repository update test"
    repository.update(fetched)

    updated = repository.get_by_id(task.id)
    print("Updated:", updated.description)
    print("Updated status:", updated.status)

    tasks = repository.list()
    print("Total tasks:", len(tasks))