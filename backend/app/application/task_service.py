from uuid import UUID

from backend.app.domain.task import Task
from backend.app.domain.task_run import TaskRun
from backend.app.infrastructure.repositories.task_repository import TaskRepository
from backend.app.infrastructure.repositories.task_run_repository import TaskRunRepository


class TaskService:

    def __init__(
        self,
        repository: TaskRepository,
        task_run_repository: TaskRunRepository,
    ):
        self.repository = repository
        self.task_run_repository = task_run_repository

    def create_task(self, description: str) -> Task:
        task = Task(description)
        return self.repository.create(task)

    def get_task(self, task_id: UUID) -> Task | None:
        return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def update_task(self, task: Task) -> Task:
        return self.repository.update(task)

    def start_task_run(self, task_id: UUID) -> TaskRun:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise ValueError(f"Task {task_id} not found")

        existing_runs = self.task_run_repository.list_by_task(task_id)
        attempt = len(existing_runs) + 1

        task_run = TaskRun(
            task_id=task_id,
            attempt=attempt,
        )
        task_run.start()
        
        return self.task_run_repository.create(task_run)

    def complete_task_run(self, run_id: UUID) -> TaskRun:
        task_run = self.task_run_repository.get_by_id(run_id)

        if task_run is None:
            raise ValueError(f"TaskRun {run_id} not found")

        task_run.complete()

        return self.task_run_repository.update(task_run)

    def fail_task_run(self, run_id: UUID, error: str) -> TaskRun:
        task_run = self.task_run_repository.get_by_id(run_id)

        if task_run is None:
            raise ValueError(f"TaskRun {run_id} not found")

        task_run.fail(error)

        return self.task_run_repository.update(task_run)

    def get_task_run(self, run_id: UUID) -> TaskRun | None:
        return self.task_run_repository.get_by_id(run_id)

    def list_task_runs(self, task_id: UUID) -> list[TaskRun]:
        return self.task_run_repository.list_by_task(task_id)