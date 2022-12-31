# repositories/user_repository.py
from web.models.user import User
from web.repositories.db_context import MongoDbContext


class UserRepository(MongoDbContext):

    def __init__(self):
        super().__init__()
        self.users = self.db.get_collection('users')

    def get_all(self):
        users = self.users.find()
        return [User(**user) for user in users]

    def create(self, data):
        self.users.insert_one(data)
        return User(**data)
