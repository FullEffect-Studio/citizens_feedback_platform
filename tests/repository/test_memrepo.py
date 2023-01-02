import pytest

from domain.user import User, UserRole
from data.repository.memrepo import MemRepo


@pytest.fixture
def users_dicts():
    return [
        {
            "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "username": "Danquah",
            "password": "pass111",
            "role": UserRole.PUBLIC_OFFICIAL
        },
        {
            "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "username": "Fahrid",
            "password": "pass222",
            "role": UserRole.PUBLIC_OFFICIAL
        },
        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Yau",
            "password": "pass333",
            "role": UserRole.ADMIN
        },

        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Lowe",
            "password": "pass444",
            "role": UserRole.COMMUNITY_SOCIAL_WORKER
        },
    ]


def test_repository_list_users_without_parameters(users_dicts):
    repo = MemRepo(users_dicts)

    users = [User.from_dict(i) for i in users_dicts]

    assert repo.list() == users


