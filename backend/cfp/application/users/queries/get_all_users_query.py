from dataclasses import dataclass

from injector import inject

from cfp.data.users.users_repository import UsersRepository
from cfp.domain.common.exceptions import HttpException
from cfp.domain.common.responses import ResponseSuccess


@dataclass
class GetAllUsersQuery:

    @inject
    def execute(self, users_repo: UsersRepository):

        try:
            users = users_repo.get_all()
            return ResponseSuccess(value=[user.dict() for user in users])
        except Exception as e:
            raise HttpException(f'Failed to query users: {e}', 401)
