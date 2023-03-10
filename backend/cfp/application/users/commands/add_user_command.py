from dataclasses import dataclass
from uuid import uuid4

from injector import inject
from pymongo.errors import DuplicateKeyError
from werkzeug.security import generate_password_hash

from cfp.data.users.users_repository import UsersRepository
from cfp.domain.common.exceptions import HttpException
from cfp.domain.common.responses import ResponseSuccess
from cfp.domain.dtos.add_user_dto import AddUserDto
from cfp.domain.user import User


@dataclass
class AddUserCommand:
    payload: AddUserDto

    @inject
    def execute(self, user_repo: UsersRepository):

        # check if username exist
        user_name_exist = user_repo.check_if_username_exist(self.payload.username)
        print('username check results', user_name_exist)
        if user_name_exist is True:
            raise HttpException(message='Specified username already exist', status_code=400)

        hashed_password = generate_password_hash(self.payload.password)

        user = User(
            id=uuid4(),
            username=self.payload.username,
            role=self.payload.role,
            password=hashed_password
        )

        try:
            user_repo.add(domain_user=user)
            return ResponseSuccess(user.to_dict())
        except DuplicateKeyError as e:
            print('An error occurred saving user: ', e)
            raise ValueError('Duplicate Ids are not allowed')
        except Exception:
            raise HttpException('An error occurred while adding user', 401)



