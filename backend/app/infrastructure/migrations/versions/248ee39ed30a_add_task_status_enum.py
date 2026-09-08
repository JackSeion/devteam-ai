"""add task status enum

Revision ID: 248ee39ed30a
Revises: 
Create Date: 2026-09-08 08:21:16.391100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '248ee39ed30a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    task_status = sa.Enum(
        'CREATED',
        'QUEUED',
        'RUNNING',
        'TESTING',
        'COMPLETED',
        'FAILED',
        name='task_status',
    )

    task_status.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        'tasks',
        'status',
        existing_type=sa.VARCHAR(length=20),
        type_=task_status,
        postgresql_using='status::task_status',
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        'tasks',
        'status',
        existing_type=sa.Enum(
            'CREATED',
            'QUEUED',
            'RUNNING',
            'TESTING',
            'COMPLETED',
            'FAILED',
            name='task_status',
        ),
        type_=sa.VARCHAR(length=20),
        postgresql_using='status::text',
        existing_nullable=False,
    )

    sa.Enum(
        'CREATED',
        'QUEUED',
        'RUNNING',
        'TESTING',
        'COMPLETED',
        'FAILED',
        name='task_status',
    ).drop(op.get_bind(), checkfirst=True)