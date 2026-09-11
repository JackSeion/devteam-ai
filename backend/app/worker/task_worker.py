from backend.app.application.queue.task_queue import TaskQueue


class TaskWorker:

    def __init__(self, task_queue: TaskQueue):
        self.task_queue = task_queue

    def process_next(self) -> None:
        job = self.task_queue.dequeue()

        if job is None:
            return

        print("Worker received job")
        print("Task ID:", job.task_id)
        print("TaskRun ID:", job.task_run_id)