from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone


class TaskRunStatus(str, Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class TaskRun:
    def __init__(self, task_id: UUID, attempt: int):
        self.id: UUID = uuid4()
        self.task_id = task_id
        self.attempt = attempt
        self.status = TaskRunStatus.CREATED
        self.created_at: datetime = datetime.now(timezone.utc)
        self.started_at: datetime | None = None
        self.finished_at: datetime | None = None
        self.error: str | None = None

    def start(self):
        if self.status != TaskRunStatus.CREATED:
            raise ValueError(
                f"Invalid transition from  {self.status} -> {TaskRunStatus.RUNNING}"
            )
        self._transition(TaskRunStatus.RUNNING)
        self.started_at = datetime.now(timezone.utc)

    def complete(self):
        if self.status != TaskRunStatus.RUNNING:
            raise ValueError(
                f"Invalid transition from  {self.status} -> {TaskRunStatus.COMPLETED}"
            )
        self._transition(TaskRunStatus.COMPLETED)
        self.finished_at = datetime.now(timezone.utc)

    def fail(self, error: str):
        if self.status != TaskRunStatus.RUNNING:
            raise ValueError(
                f"Invalid transition from  {self.status} -> {TaskRunStatus.FAILED}"
            )
        self._transition(TaskRunStatus.FAILED)
        self.error = error
        self.finished_at = datetime.now(timezone.utc)

    def _transition(self, new_status: TaskRunStatus):
        allowed = {
            TaskRunStatus.CREATED: [TaskRunStatus.RUNNING],
            TaskRunStatus.RUNNING: [
                TaskRunStatus.COMPLETED,
                TaskRunStatus.FAILED,
            ],
            TaskRunStatus.COMPLETED: set(),
            TaskRunStatus.FAILED: set(),
        }

        if new_status not in allowed[self.status]:
            raise ValueError(
                f"Invalid transition from {self.status} -> {new_status}"
            )

        self.status = new_status