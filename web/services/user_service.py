# services/user_service.py
from web.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def create(self, data):
        return self.repository.create(data)
