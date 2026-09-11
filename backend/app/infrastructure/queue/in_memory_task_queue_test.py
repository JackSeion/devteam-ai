from uuid import uuid4

from backend.app.domain.task_job import TaskJob
from backend.app.infrastructure.queue.in_memory_task_queue import InMemoryTaskQueue


queue = InMemoryTaskQueue()

job1 = TaskJob(uuid4(), uuid4())
job2 = TaskJob(uuid4(), uuid4())

queue.enqueue(job1)
queue.enqueue(job2)

first = queue.dequeue()
second = queue.dequeue()
empty = queue.dequeue()

print("First:", first)
print("Second:", second)
print("Empty:", empty)