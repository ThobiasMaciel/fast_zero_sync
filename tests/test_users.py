from http import HTTPStatus

from src.fast_zero.models import User
from src.fast_zero.schemas import UserPublicSchema


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


# Função auxiliar para pegar o header de autorização com token válido
def get_auth_header(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
            'scope': '',
        },
    )
    token = response.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_read_users(client, user):
    headers = get_auth_header(client, user)
    response = client.get('/users', headers=headers)
    assert response.status_code == HTTPStatus.OK

    expected = {'users': [UserPublicSchema.model_validate(user).model_dump()]}
    assert response.json() == expected


def test_read_users_with_users(client, user):
    # Reuso do mesmo teste para garantir usuários na lista
    headers = get_auth_header(client, user)
    response = client.get('/users/', headers=headers)
    assert response.status_code == HTTPStatus.OK
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    headers = get_auth_header(client, user)

    response = client.put(
        f'/users/{user.id}',
        json={
            'username': 'bob',
            'email': 'bob@test.com',
            'password': 'mynewpassword',
        },
        headers=headers,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'bob',
        'email': 'bob@test.com',
    }


def test_delete_user(client, user):
    headers = get_auth_header(client, user)
    response = client.delete(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_integrity_error(client, session, user):
    existing_user = User(
        username='existinguser',
        email='existing@test.com',
        password='123',
    )
    session.add(existing_user)
    session.commit()

    headers = get_auth_header(client, user)

    response_update = client.put(
        f'/users/{user.id}',
        headers=headers,
        json={
            'id': user.id,
            'username': 'existinguser',
            'email': 'newemail@test.com',
            'password': '123',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {'detail': 'Username already exists'}
