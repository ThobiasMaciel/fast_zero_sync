from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.fast_zero.database import get_session
from src.fast_zero.models import Todo, TodoPriority, TodoState, User
from src.fast_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from src.fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[Session, Depends(get_session)]
User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic, status_code=HTTPStatus.CREATED)
def create_todo(
    todo: TodoSchema,
    session: Session,
    user: User,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        priority=todo.priority,
        due_date=todo.due_date,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


class TodoFilters(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
    priority: TodoPriority | None = None
    due_before: datetime | None = None
    offset: int = 0
    limit: int = 100


@router.get('/', response_model=TodoList)
def list_todos(
    session: Session,
    user: User,
    filters: TodoFilters = Depends(),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if filters.title:
        query = query.filter(Todo.title.contains(filters.title))

    if filters.description:
        query = query.filter(Todo.description.contains(filters.description))

    if filters.state:
        query = query.filter(Todo.state == filters.state)

    if filters.priority:
        query = query.filter(Todo.priority == filters.priority)

    if filters.due_before:
        query = query.filter(Todo.due_date <= filters.due_before)

    todos = session.scalars(
        query.offset(filters.offset).limit(filters.limit)
    ).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: Session, user: User):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()  # <<< Commit adicionado

    return {'message': 'Task has been deleted successfully.'}


@router.get('/{todo_id}', response_model=TodoPublic)
def get_task_by_id(
    todo_id: int,  # ✅ Corrigido aqui
    session: Session,
    user: User,
):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Task not found',
        )

    return todo


@router.patch('/{todo_id}', response_model=TodoPublic)
async def patch_todo(
    todo_id: int, session: Session, user: User, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
