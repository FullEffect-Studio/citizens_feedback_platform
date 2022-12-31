from uuid import uuid4
from unittest.mock import MagicMock, Mock

import pytest

from app.domain.user import User
from app.requests.user_list import UserListRequest
from app.usecases.user_list import user_list_usecase


@pytest.fixture
def domain_users():
    user_1 = User(
        id=uuid4(),
        username="Danquah",
        password="pass111"
    )

    user_2 = User(
        id=uuid4(),
        username="Fahrid",
        password="pass222"
    )

    user_3 = User(
        id=uuid4(),
        username="Yau",
        password="pass333"
    )

    user_4 = User(
        id=uuid4(),
        username="Lowe",
        password="pass444"
    )

    return [user_1, user_2, user_3, user_4]


def test_room_list_without_parameters(domain_users):
    repo = Mock()
    repo.list.return_value = domain_users

    request = UserListRequest()

    response = user_list_usecase(repo, request)

    assert bool(response) is True

    repo.list.assert_called_with()

    assert response.value == domain_users
