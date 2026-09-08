from backend.app.domain.task import Task, TaskStatus


task = Task("Test task lifecycle")

print(task.status)

task.queue()
print(task.status)

task.start()
print(task.status)

task.start_testing()
print(task.status)

task.complete()
print(task.status)