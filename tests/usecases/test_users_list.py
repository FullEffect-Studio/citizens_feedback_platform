from uuid import uuid4
from unittest.mock import MagicMock, Mock

import pytest

from app.domain.user import User, UserRole
from app.requests.user_list import build_user_list_request
from app.responses import ResponseTypes
from app.usecases.user_list import user_list_usecase


@pytest.fixture
def domain_users():
    user_1 = User(
        id=uuid4(),
        username="Danquah",
        password="pass111",
        role=UserRole.COMMUNITY_SOCIAL_WORKER
    )

    user_2 = User(
        id=uuid4(),
        username="Fahrid",
        password="pass222",
        role=UserRole.PUBLIC_OFFICIAL
    )

    user_3 = User(
        id=uuid4(),
        username="Yau",
        password="pass333",
        role=UserRole.PUBLIC_OFFICIAL
    )

    user_4 = User(
        id=uuid4(),
        username="Lowe",
        password="pass444",
        role=UserRole.ADMIN
    )

    return [user_1, user_2, user_3, user_4]


def test_room_list_without_parameters(domain_users):
    repo = Mock()
    repo.list.return_value = domain_users

    request = build_user_list_request()

    response = user_list_usecase(repo, request)

    assert bool(response) is True

    repo.list.assert_called_with(filters=None)

    assert response.value == domain_users

def test_user_list_with_filters(domain_users):
    repo = Mock()
    repo.list.return_value = domain_users

    qry_filters = {"role__eq": "Administrator"}
    request = build_user_list_request(filters=qry_filters)

    response = user_list_usecase(repo, request)

    assert bool(response) is True
    repo.list.assert_called_with(filters=qry_filters)
    assert response.value == domain_users


def test_user_list_handles_generic_error():
    repo = Mock()
    repo.list.side_effect = Exception('Just an error message')

    request = build_user_list_request(filters={})

    response = user_list_usecase(repo, request)

    assert bool(response) is False

    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": "Exception: Just an error message"
    }

def test_room_list_handles_bad_request():
    repo = Mock()

    request = build_user_list_request(filters=5)

    response = user_list_usecase(repo, request)

    assert bool(response) is False
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": "filters: Is not iterable",
    }
