from abc import ABC, abstractmethod

from backend.app.domain.task_job import TaskJob

class TaskQueue(ABC):
    @abstractmethod
    def enqueue(self, task_job: TaskJob) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> TaskJob | None:
        pass