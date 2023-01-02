from unittest.mock import Mock

import pytest

from domain.user import UserRole
from application.dtos.user_list_dto import UserListDto
from domain.usecases.user_list import user_list_usecase


@pytest.fixture
def dto_user_list():
    user_1 = UserListDto(
        id="f853578c-fc0f-4e65-81b8-566c5dffa35a",
        username="Danquah",
        role=UserRole.COMMUNITY_SOCIAL_WORKER
    )

    user_2 = UserListDto(
        id="fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        username="Fahrid",
        role=UserRole.PUBLIC_OFFICIAL
    )

    user_3 = UserListDto(
        id="913694c6-435a-4366-ba0d-da5334a611b2",
        username="Yau",
        role=UserRole.PUBLIC_OFFICIAL
    )

    user_4 = UserListDto(
        id="913694c6-435a-4366-ba0d-da5334a611b2",
        username="Lowe",
        role=UserRole.ADMIN
    )

    return [user_1, user_2, user_3, user_4]


def test_room_list_without_parameters(dto_user_list):
    repo = Mock()
    repo.list.return_value = dto_user_list

    response = user_list_usecase(repo)

    # print(response)
    assert bool(response) is True

    repo.list.assert_called_with()

    assert response.value == dto_user_list
