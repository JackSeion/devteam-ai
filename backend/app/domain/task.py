from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    CREATED="CREATED" 
    QUEUED="QUEUED"
    RUNNING="RUNNING"
    TESTING="TESTING"
    COMPLETED="COMPLETED"
    FAILED="FAILED"

class Task:
    def __init__(self, description: str):
        self.id: UUID = uuid4()
        self.description = description
        self.status = TaskStatus.CREATED
        self.created_at: datetime = datetime.now(timezone.utc)

    def queue(self):
        self._transition(TaskStatus.QUEUED)

    def start(self):
        self._transition(TaskStatus.RUNNING)

    def start_testing(self):
        self._transition(TaskStatus.TESTING)

    def complete(self):
        self._transition(TaskStatus.COMPLETED)

    def fail(self):
        self._transition(TaskStatus.FAILED)

    def _transition(self, new_status: TaskStatus):
        allowed = {
            TaskStatus.CREATED: [TaskStatus.QUEUED],
            TaskStatus.QUEUED: [TaskStatus.RUNNING],
            TaskStatus.RUNNING: [TaskStatus.TESTING, TaskStatus.FAILED],
            TaskStatus.TESTING: [TaskStatus.COMPLETED, TaskStatus.FAILED],
            TaskStatus.COMPLETED: set(),
            TaskStatus.FAILED: set(),
        }

        if new_status not in allowed[self.status]:
            raise ValueError(f"Invalid transition from {self.status} -> {new_status}")

        self.status = new_status