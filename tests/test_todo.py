from http import HTTPStatus

from src.fast_zero.models import TaskState
from tests.conftest import TaskFactory


def test_create_todo(client, token):
    response = client.post(
        '/task/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test task',
            'description': 'Test task description',
            'state': 'draft',
            'priority': 'low',
            'due_data': None,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test task',
        'description': 'Test task description',
        'state': 'draft',
        'priority': 'low',
        'due_date': None,
    }


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_task = 5
    session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/task/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['task']) == expected_task


def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    expected_tasks = 2
    session.add_all(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/task/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['task']) == expected_tasks


def test_list_todos_filter_title_should_return_5_todos(
    session, user, client, token
):
    expected_task = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, title='Test task 1')
    )
    session.commit()

    response = client.get(
        '/task/?title=Test task 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['task']) == expected_task


def test_list_todos_filter_description_should_return_5_todos(
    session, user, client, token
):
    expected_task = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, description='description')
    )
    session.commit()

    response = client.get(
        '/task/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['task']) == expected_task


def test_list_todos_filter_state_should_return_5_todos(
    session, user, client, token
):
    expected_task = 5
    session.add_all(
        TaskFactory.create_batch(5, user_id=user.id, state=TaskState.draft)
    )
    session.commit()

    response = client.get(
        '/task/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['task']) == expected_task


def test_delete_todo(session, client, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    session.commit()

    response = client.delete(
        f'/task/{task.user_id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


def test_get_todo_by_id(session, client, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    session.commit()

    response = client.get(
        f'/task/{task.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['id'] == task.id


def test_delete_todo_error(client, token):
    response = client.delete(
        f'/task/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/task/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, client, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    session.commit()

    response = client.patch(
        f'/task/{task.user_id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'
