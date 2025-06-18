from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from src.fast_zero.models import TaskPriority, TaskState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublicSchema]


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TaskSchema(BaseModel):
    title: str
    description: str
    state: TaskState
    priority: TaskPriority
    due_date: Optional[datetime] = None


class TaskPublic(TaskSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    task: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
    priority: TaskPriority | None = None
    due_date: Optional[datetime] = None
