# services/user_service.py
from models.user import User


class UserService:

    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def create(self, payload):
        data = User()
        return self.repository.create(data)
