from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token',
        data={
            'username': user.email,
            'password': user.clean_password,
            'scope': '',
        },
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'].lower() == 'bearer'
    assert 'access_token' in token
