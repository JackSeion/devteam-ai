import uuid
from datetime import datetime, timezone

from backend.app.infrastructure.database import SessionLocal
from backend.app.infrastructure.models import TaskModel


task = TaskModel(
    id=uuid.uuid4(),
    description="ORM created task",
    status="CREATED",
    created_at=datetime.now(timezone.utc),
)

with SessionLocal() as session:
    session.add(task)
    session.commit()

    print("Created:", task.id)