from backend.app.application.task_service import TaskService
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.repositories.task_run_repository import TaskRunRepository
from backend.app.infrastructure.queue.in_memory_task_queue import InMemoryTaskQueue

with SessionLocal() as session:
    repository = TaskRepository(session)
    task_run_repository = TaskRunRepository(session)
    task_queue = InMemoryTaskQueue()

    service = TaskService(repository, task_run_repository, task_queue)

    task = service.create_task("Test task service")

    print("Created:", task.id)
    print("Description:", task.description)
    print("Status:", task.status)

    fetched = service.get_task(task.id)

    print("Fetched:", fetched.id)
    print("Fetched description:", fetched.description)

    tasks = service.list_tasks()

    task_run = service.start_task_run(task.id)

    print("TaskRun:", task_run.id)
    print("TaskRun task:", task_run.task_id)
    print("TaskRun attempt:", task_run.attempt)
    print("TaskRun status:", task_run.status) 

    job = task_queue.dequeue()

    print("Queued job:", job)

    completed_run = service.complete_task_run(task_run.id)

    print("Completed status:", completed_run.status)
    print("Finished at:", completed_run.finished_at)

    retry_run = service.start_task_run(task.id)

    print("Retry TaskRun:", retry_run.id)
    print("Retry attempt:", retry_run.attempt)
    print("Retry status:", retry_run.status)

    failed_run = service.fail_task_run(
        retry_run.id,
        "Test failure"
    )

    print("Failed status:", failed_run.status)
    print("Error:", failed_run.error)
    print("Finished at:", failed_run.finished_at)

    runs = task_run_repository.list_by_task(task.id)

    print("Total runs:", len(runs))

    for run in runs:
        print(
            "Run:",
            run.attempt,
            "| Status:",
            run.status,
            "| Error:",
            run.error,
        )