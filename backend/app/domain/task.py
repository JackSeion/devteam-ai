from enum import Enum
from uuid import UUID, uuid4

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