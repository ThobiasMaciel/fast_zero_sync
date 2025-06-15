from http import HTTPStatus

from src.fast_zero.models import User
from src.fast_zero.schemas import UserPublicSchema


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': '<PASSWORD>',
            'email': 'testEMail@test.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testEMail@test.com',
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):  # <-- adiciona a fixture user aqui
    response = client.put(
        f'/users/{user.id}',
        json={
            'id': user.id,
            'username': 'testuser',
            'email': 'testEMail@test.com',
            'password': '123',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'testuser',
        'email': 'testEMail@test.com',
    }


def test_delete_user(client, user):  # também aqui
    response = client.delete(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, session, user):
    existing_user = User(
        username='existinguser', email='existing@test.com', password='123'
    )
    session.add(existing_user)
    session.commit()

    response_update = client.put(
        f'/users/{user.id}',
        json={
            'id': user.id,
            'username': 'existinguser',  # Nome que já existe
            'email': 'newemail@test.com',
            'password': '123',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username already exists'}
