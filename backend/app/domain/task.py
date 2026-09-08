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