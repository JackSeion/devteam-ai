from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TaskJob:
    task_id: UUID
    task_run_id: UUID