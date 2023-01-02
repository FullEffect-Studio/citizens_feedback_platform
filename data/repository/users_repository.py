from injector import inject
from marshmallow import Schema, fields

from data.repository.mongo_client import AppMongoClient
from domain.user import User
from data.repository.mongo_base import BaseRepository


class UsersRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.users = self.client.get_default_database().get_collection('users')

    def list(self):
        result = self.users.find()
        return [
            User(
                id=q['id'],
                username=q['username'],
                password=q['password'],
                role=q['role']
            )
            for q in result
        ]

    def add(self, domain_user: User):

        data = domain_user.to_dict()
        data['id'] = str(domain_user.id)

        result = self.users.insert_one(data)

        return str(result.inserted_id)
