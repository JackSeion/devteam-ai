from backend.app.application.task_service import TaskService
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.repositories.task_repository import TaskRepository


with SessionLocal() as session:
    repository = TaskRepository(session)
    service = TaskService(repository)

    task = service.create_task("Test task service")

    print("Created:", task.id)
    print("Description:", task.description)
    print("Status:", task.status)

    fetched = service.get_task(task.id)

    print("Fetched:", fetched.id)
    print("Fetched description:", fetched.description)

    tasks = service.list_tasks()

    print("Total tasks:", len(tasks))