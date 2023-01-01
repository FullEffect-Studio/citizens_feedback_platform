from uuid import uuid4
from unittest.mock import MagicMock, Mock

import pytest

from app.domain.user import User, UserRole
from app.dtos.user_list_dto import UserListDto
from app.usecases.user_list import user_list_usecase


@pytest.fixture
def dto_user_list():
    user_1 = UserListDto(
        id="f853578c-fc0f-4e65-81b8-566c5dffa35a",
        username="Danquah",
        role=UserRole.COMMUNITY_SOCIAL_WORKER
    )

    # user_2 = UserListDto(
    #     id=uuid4(),
    #     username="Fahrid",
    #     role=UserRole.PUBLIC_OFFICIAL
    # )
    #
    # user_3 = UserListDto(
    #     id=uuid4(),
    #     username="Yau",
    #     role=UserRole.PUBLIC_OFFICIAL
    # )
    #
    # user_4 = UserListDto(
    #     id=uuid4(),
    #     username="Lowe",
    #     role=UserRole.ADMIN
    # )

    return [user_1]
            # user_2, user_3, user_4]


def test_room_list_without_parameters(dto_user_list):
    repo = Mock()
    repo.list.return_value = dto_user_list

    response = user_list_usecase(repo)

    # print(response)
    assert bool(response) is True

    repo.list.assert_called_with()

    assert response.value == dto_user_list
