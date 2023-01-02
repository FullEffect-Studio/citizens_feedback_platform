from dataclasses import dataclass

from flask_jwt_extended import create_access_token, create_refresh_token
from injector import inject
from werkzeug.security import check_password_hash

from application.dtos.user_list_dto import UserInListDto
from data.users.users_repository import UsersRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from application.dtos.login_credentials_dto import LoginCredentialsDto


@dataclass
class LoginUserCommand:
    payload: LoginCredentialsDto

    @inject
    def execute(self, user_repo: UsersRepository):

        user = user_repo.find_by_username(self.payload.username)
        if not user:
            raise HttpException(message='Invalid credentials', status_code=401)

        if check_password_hash(user.password, self.payload.password):
            auth_payload = UserInListDto(
                id=user.id,
                username=user.username,
                role=user.role
            )
            access_token = create_access_token(identity=auth_payload.dict())
            refresh_token = create_refresh_token(identity=auth_payload.dict())

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            raise HttpException(message="Invalid password", status_code=401)
