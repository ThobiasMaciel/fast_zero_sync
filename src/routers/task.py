from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import Task, TaskPriority, TaskState, User
from src.fast_zero.schemas import (
    Message,
    TaskList,
    TaskPublic,
    TaskSchema,
    TaskUpdate,
)
from src.fast_zero.security import get_current_user

router = APIRouter(prefix='/task', tags=['task'])

Session = Annotated[Session, Depends(get_session)]
User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TaskPublic, status_code=HTTPStatus.CREATED)
def create_todo(
    task: TaskSchema,
    session: Session,
    user: User,
):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user.id,
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


class TaskFilters(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
    priority: TaskPriority | None = None
    due_before: datetime | None = None
    offset: int = 0
    limit: int = 100


@router.get('/', response_model=TaskList)
def list_todos(
    session: Session,
    user: User,
    filters: TaskFilters = Depends(),
):
    query = select(Task).where(Task.user_id == user.id)

    if filters.title:
        query = query.filter(Task.title.contains(filters.title))

    if filters.description:
        query = query.filter(Task.description.contains(filters.description))

    if filters.state:
        query = query.filter(Task.state == filters.state)

    if filters.priority:
        query = query.filter(Task.priority == filters.priority)

    if filters.due_before:
        query = query.filter(Task.due_date <= filters.due_before)

    task = session.scalars(
        query.offset(filters.offset).limit(filters.limit)
    ).all()

    return {'task': task}


@router.get('/{task_id}', response_model=TaskPublic)
def get_task_by_id(
    task_id: int,
    session: Session,
    user: User,
):
    task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found',
        )

    return task


@router.patch('/{task_id}', response_model=TaskPublic)
def patch_todo(task_id: int, session: Session, user: User, todo: TaskUpdate):
    db_task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not db_task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete('/{task_id}', response_model=Message)
def delete_todo(task_id: int, session: Session, user: User):
    task = session.scalar(
        select(Task).where(Task.user_id == user.id, Task.id == task_id)
    )

    if not task:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(task)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}
