from backend.app.application.queue.task_queue import TaskQueue
from backend.app.application.task_service import TaskService 

class TaskWorker:

    def __init__(self, task_queue: TaskQueue, task_service: TaskService):
        self.task_queue = task_queue
        self.task_service = task_service

    def process_next(self) -> None:
        job = self.task_queue.dequeue()

        if job is None:
            return

        print("Worker received job")
        print("Task ID:", job.task_id)
        print("TaskRun ID:", job.task_run_id)

        task_run = self.task_service.execute_task_run(
            job.task_run_id
        )


        print("TaskRun completed")
        print("Status:", task_run.status)        