from domain.user import UserRole
from data.repository.memrepo import MemRepo
from domain.usecases.user_list import user_list_usecase
from pprint import pprint as pp
data_source = [
    {
        "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "username": "Danquah",
        "password": "pass111",
        "role": UserRole.ADMIN
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
repo = MemRepo(data_source)
try:
    result = user_list_usecase(repo)
    pp([user for user in result.value], indent=4)
except :
    print('Ops! an error occurred while getting list of users')


