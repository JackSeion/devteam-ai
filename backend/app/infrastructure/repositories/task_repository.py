from uuid import UUID

from sqlalchemy import select

from backend.app.domain.task import Task
from backend.app.infrastructure.models import TaskModel


class TaskRepository:

    def __init__(self, session):
        self.session = session

    def create(self, task: Task) -> Task:
        task_model = TaskModel(
            id=task.id,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )

        self.session.add(task_model)
        self.session.commit()

        return task

    def get_by_id(self, task_id: UUID) -> Task | None:
        statement = select(TaskModel).where(TaskModel.id == task_id)
        task_model = self.session.execute(statement).scalar_one_or_none()

        if task_model is None:
            return None

        return self._to_domain(task_model)

    def list(self) -> list[Task]:
        statement = select(TaskModel).order_by(TaskModel.created_at)
        task_models = self.session.execute(statement).scalars().all()

        return [self._to_domain(task_model) for task_model in task_models]

    def update(self, task: Task) -> Task:
        task_model = self.session.get(TaskModel, task.id)

        if task_model is None:
            raise ValueError(f"Task {task.id} not found")

        task_model.description = task.description
        task_model.status = task.status

        self.session.commit()

        return task

    @staticmethod
    def _to_domain(task_model: TaskModel) -> Task:
        task = Task.__new__(Task)
        task.id = task_model.id
        task.description = task_model.description
        task.status = task_model.status
        task.created_at = task_model.created_at

        return task