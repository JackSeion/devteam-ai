from uuid import UUID

from backend.app.domain.task import Task
from backend.app.infrastructure.repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, description: str) -> Task:
        task = Task(description)
        return self.repository.create(task)

    def get_task(self, task_id: UUID) -> Task | None:
        return self.repository.get_by_id(task_id)

    def list_tasks(self) -> list[Task]:
        return self.repository.list()

    def update_task(self, task: Task) -> Task:
        return self.repository.update(task)