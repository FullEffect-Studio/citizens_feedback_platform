from uuid import uuid4

from app.domain.user import User


def test_user_model_init():
    code = uuid4()
    user = User(
        id=code,
        username='Ben',
        password='qwe123!'
    )

    assert user.id == code
    assert user.username == 'Ben'
    assert user.password == 'qwe123!'


def test_user_model_from_dict():
    code = uuid4()
    dict_data = {
        "id": code,
        "username": "Ben",
        "password": "qwe123!"
    }

    user = User.from_dict(dict_data)
    assert user.id == code
    assert user.username == 'Ben'
    assert user.password == 'qwe123!'


def test_user_model_to_dict():
    dict_data = {
        "id": uuid4(),
        "username": "Ben",
        "password": "qwe123!"
    }

    user = User.from_dict(dict_data)
    assert user.to_dict() == dict_data


def test_user_comparison():
    dict_data = {
        "id": uuid4(),
        "username": "Ben",
        "password": "qwe123!"
    }

    user1 = User.from_dict(dict_data)
    user2 = User.from_dict(dict_data)

    assert user1 == user2