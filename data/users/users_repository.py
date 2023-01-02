import pprint

from injector import inject

from data.mongo_client import AppMongoClient
from data.users.user_data import UserData
from domain.user import User
from data.mongo_base import BaseRepository


class UsersRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.users = self.client.get_default_database().get_collection('users')

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
        data['id'] = str(domain_user.id)
        pprint.pprint(data)

        try:
            print(UserData(**data))
            model = UserData(**data).save()
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
        print('checking for username', username)
        try:

            result = self.users.find_one({'username': username})
            if result is not None:
                return True

            return False
        except Exception as e:
            raise e
