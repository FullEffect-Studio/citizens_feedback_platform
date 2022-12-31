from app.repository.memrepo import MemRepo
from app.usecases.users_list import users_list_usecase

data_source = [
        {
            "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
            "username": "Danquah",
            "password": "pass111"
        },
        {
            "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
            "username": "Fahrid",
            "password": "pass222"
        },
        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Yau",
            "password": "pass333"
        },

        {
            "id": "913694c6-435a-4366-ba0d-da5334a611b2",
            "username": "Lowe",
            "password": "pass444"
        },
    ]
repo = MemRepo(data_source)
result = users_list_usecase(repo)

print([user.to_dict() for user in result])

