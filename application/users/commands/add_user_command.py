from dataclasses import dataclass
from uuid import uuid4

from injector import inject

from application.responses import ResponseFailure, ResponseTypes, ResponseSuccess
from data.repository.users_repository import UsersRepository
from domain.user import User
from web.controllers.add_user_dto import AddUserDto


@dataclass
class AddUserCommand:
    payload: AddUserDto

    @inject
    def execute(self, user_repo: UsersRepository):

        # generate a random password and Hash it

        user = User(
            id=uuid4(),
            username=self.payload.username,
            role=self.payload.role,
            password=self.payload.password
        )

        try:
            user = user_repo.add(domain_user=user)
        except Exception as e:
            print('An error occurred saving user', e)
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, e)

        print('save user in db result', user)
        return ResponseSuccess()

