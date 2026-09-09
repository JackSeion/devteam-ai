from uuid import UUID

from sqlalchemy import select

from backend.app.domain.task_run import TaskRun, TaskRunStatus
from backend.app.infrastructure.models import TaskRunModel


class TaskRunRepository:

    def __init__(self, session):
        self.session = session

    def create(self, task_run: TaskRun) -> TaskRun:
        task_run_model = TaskRunModel(
            id=task_run.id,
            task_id=task_run.task_id,
            attempt=task_run.attempt,
            status=task_run.status,
            created_at=task_run.created_at,
            started_at=task_run.started_at,
            finished_at=task_run.finished_at,
            error=task_run.error,
        )

        self.session.add(task_run_model)
        self.session.commit()

        return task_run

    def get_by_id(self, run_id: UUID) -> TaskRun | None:
        statement = select(TaskRunModel).where(
            TaskRunModel.id == run_id
        )

        task_run_model = self.session.execute(
            statement
        ).scalar_one_or_none()

        if task_run_model is None:
            return None

        return self._to_domain(task_run_model)

    def update(self, task_run: TaskRun) -> TaskRun:
        task_run_model = self.session.get(TaskRunModel, task_run.id)

        if task_run_model is None:
            raise ValueError(f"TaskRun {task_run.id} not found")

        task_run_model.status = task_run.status
        task_run_model.started_at = task_run.started_at
        task_run_model.finished_at = task_run.finished_at
        task_run_model.error = task_run.error

        self.session.commit()

        return task_run

    def list_by_task(self, task_id: UUID) -> list[TaskRun]:
        statement = (
            select(TaskRunModel)
            .where(TaskRunModel.task_id == task_id)
            .order_by(TaskRunModel.attempt)
        )

        task_run_models = self.session.execute(
            statement
        ).scalars().all()

        return [
            self._to_domain(task_run_model)
            for task_run_model in task_run_models
        ]

    @staticmethod
    def _to_domain(task_run_model: TaskRunModel) -> TaskRun:
        task_run = TaskRun.__new__(TaskRun)

        task_run.id = task_run_model.id
        task_run.task_id = task_run_model.task_id
        task_run.attempt = task_run_model.attempt
        task_run.status = TaskRunStatus(task_run_model.status)
        task_run.created_at = task_run_model.created_at
        task_run.started_at = task_run_model.started_at
        task_run.finished_at = task_run_model.finished_at
        task_run.error = task_run_model.error

        return task_run