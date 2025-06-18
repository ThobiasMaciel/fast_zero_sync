from http import HTTPStatus

from fastapi import FastAPI

from src.fast_zero.schemas import (
    Message,
)
from src.routers import auth, task, users

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(task.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World!'}
