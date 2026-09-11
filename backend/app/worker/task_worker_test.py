from uuid import uuid4

from backend.app.domain.task_job import TaskJob
from backend.app.infrastructure.queue.in_memory_task_queue import InMemoryTaskQueue
from backend.app.worker.task_worker import TaskWorker


queue = InMemoryTaskQueue()

job = TaskJob(
    task_id=uuid4(),
    task_run_id=uuid4(),
)

queue.enqueue(job)

worker = TaskWorker(queue)

worker.process_next()
worker.process_next()