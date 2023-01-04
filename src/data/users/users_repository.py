import pprint

from injector import inject

from src.application.dtos.user_list_dto import UserInListDto
from src.data.mongo_client import AppMongoClient
from src.data.users.user_data import UserData
from src.domain.user import User
from src.data.mongo_base import BaseRepository


class UsersRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.users = self.client.get_default_database().get_collection('users')

    def get_all(self):
        try:
            result = self.users.find()
            return [
                UserInListDto(
                    id=data['_id'],
                    username=data['username'],
                    role=data['role']
                ) for data in result]
        except Exception as e:
            print(e)
            raise e

    def add(self, domain_user: User):
        data = domain_user.to_dict()
        data['id'] = str(domain_user.id)
        pprint.pprint(data)

        try:
            # print(UserData(**data))
            model = UserData(**data).save()
        except Exception as e:
            print(e)
            raise e

    def find_by_username(self, username):
        try:
            result = self.users.find_one({'username': username})
            if result is not None:
                return self._build_user(result)
            return None
        except Exception as e:
            raise e

    def check_if_username_exist(self, username) -> bool:
        # print('checking for username', username)
        try:

            result = self.users.find_one({'username': username})
            if result is not None:
                return True

            return False
        except Exception as e:
            raise e

    def _build_user(self, data):
        return User(
            id=data['_id'],
            username=data['username'],
            password=data['password'],
            role=data['role']
        )
