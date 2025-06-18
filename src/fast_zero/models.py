from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class TaskPriority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class TaskState(str, Enum):
    draft = 'draft'
    task = 'task'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )


# ...


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TaskState]
    priority: Mapped[TaskPriority]
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
