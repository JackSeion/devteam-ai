from backend.app.application.task_service import TaskService
from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.queue.in_memory_task_queue import InMemoryTaskQueue
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.repositories.task_run_repository import TaskRunRepository
from backend.app.worker.task_worker import TaskWorker


with SessionLocal() as session:
    task_repository = TaskRepository(session)
    task_run_repository = TaskRunRepository(session)
    task_queue = InMemoryTaskQueue()

    task_service = TaskService(
        task_repository,
        task_run_repository,
        task_queue,
    )

    task = task_service.create_task("Test worker execution")

    task_run = task_service.start_task_run(task.id)

    print("Created TaskRun:", task_run.id)
    print("Initial status:", task_run.status)

    worker = TaskWorker(
        task_queue,
        task_service,
    )

    worker.process_next()

    updated_run = task_run_repository.get_by_id(task_run.id)

    print("Final status:", updated_run.status)
    print("Finished at:", updated_run.finished_at)