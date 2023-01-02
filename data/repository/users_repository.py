import pprint

from bson import Binary
from injector import inject
from marshmallow import Schema, fields
from pymongo.errors import DuplicateKeyError

from data.repository.mongo_client import AppMongoClient
from domain.user import User
from data.repository.mongo_base import BaseRepository


class UsersRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)

        # self.client.get_default_database().create_collection('users', idIndex={'key': {'id': 1}, 'unique': True}, check_exists=True)
        self.users = self.client.get_default_database().get_collection('users')
        # print('users_index_information', sorted(list(self.users.index_information())))

    def list(self):
        result = self.users.find()
        return [
            User(
                id=q['_id'],
                username=q['username'],
                password=q['password'],
                role=q['role']
            )
            for q in result
        ]

    def add(self, domain_user: User):

        data = domain_user.to_dict()
        data['_id'] = str(domain_user.id)
        data['id'] = str(domain_user.id)
        pprint.pprint(data)

        try:
            result = self.users.insert_one(data)
            return str(result.inserted_id)
        except Exception as e:
            print(e)
            raise e

    def find_by_username(self, username):
        try:
            result = self.users.find_one({'username': username})
            if result is not None:
                return User(
                    id=result['_id'],
                    username=result['username'],
                    password=result['password'],
                    role=result['role']
                )

            return None
        except Exception as e:
            raise e

    def check_if_username_exist(self, username) -> bool:
        try:
            result = self.users.find_one({'username': username})
            if result is not None:
                return True

            return False
        except Exception as e:
            raise e
