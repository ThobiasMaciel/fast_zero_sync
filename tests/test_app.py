from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users/',  # userSchema
        json={
            'username': 'testuser',
            'password': '<PASSWORD>',
            'email': 'testEMail@test.com',
        },
    )
    # voltou correto?
    assert response.status_code == HTTPStatus.CREATED
    # validar userpublic
    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testEMail@test.com',
    }


def test_read_user(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testuser',
                'email': 'testEMail@test.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'testuser',
            'email': 'testEMail@test.com',
            'password': '123',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'testuser',
        'email': 'testEMail@test.com',
    }


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
