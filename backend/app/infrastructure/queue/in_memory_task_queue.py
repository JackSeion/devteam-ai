from collections import deque

from backend.app.application.queue.task_queue import TaskQueue
from backend.app.domain.task_job import TaskJob

class InMemoryTaskQueue(TaskQueue):
    def __init__(self):
        self.jobs=deque()

    def enqueue(self, task_job: TaskJob) -> None:
        self.jobs.append(task_job)

    def dequeue(self) -> TaskJob | None:
        if self.jobs:
            return self.jobs.popleft()
        return None