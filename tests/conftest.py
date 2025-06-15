import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.fast_zero.app import app
from src.fast_zero.database import get_session
from src.fast_zero.models import User, table_registry


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
    try:
        yield db
    finally:
        db.close()
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    # Faz override do get_session para usar o session do teste
    def get_test_session():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = User(
        username='testuser', email='testEMail@test.com', password='123'
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
