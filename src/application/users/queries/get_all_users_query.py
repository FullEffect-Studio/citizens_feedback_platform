from dataclasses import dataclass

from injector import inject

from application.responses import ResponseSuccess
from data.users.users_repository import UsersRepository
from domain.exceptions import HttpException


@dataclass
class GetAllUsersQuery:

    @inject
    def execute(self, users_repo: UsersRepository):

        try:
            users = users_repo.get_all()
            return ResponseSuccess(value=[user.dict() for user in users])
        except Exception as e:
            raise HttpException(f'Failed to query users: {e}', 401)
