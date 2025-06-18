from datetime import datetime, timedelta

import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.fast_zero.app import app
from src.fast_zero.database import get_session
from src.fast_zero.models import Task, User, table_registry
from src.fast_zero.security import get_password_hash


class TaskFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Task
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'

    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    state = 'draft'
    priority = 'low'
    due_date = factory.LazyFunction(
        lambda: datetime.utcnow() + timedelta(days=7)
    )
    user_id = 1


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)

    db = SessionLocal()

    # <-- Adicione isso aqui:
    TaskFactory._meta.sqlalchemy_session = db

    try:
        yield db
    finally:
        db.close()
        table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    pwd = 'testtest'
    user = User(
        username='testuser',
        email='testEMail@test.com',
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # atributo temporário para uso no teste

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
