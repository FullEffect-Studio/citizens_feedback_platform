from dataclasses import dataclass
from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from injector import inject
from werkzeug.security import check_password_hash

from application.dtos.user_list_dto import UserInListDto
from data.users.users_repository import UsersRepository
from domain.exceptions import HttpException, BadRequestException, UnauthorizedException
from application.dtos.login_credentials_dto import LoginCredentialsDto


@dataclass
class LoginUserCommand:
    payload: LoginCredentialsDto

    @inject
    def execute(self, user_repo: UsersRepository):

        user = user_repo.find_by_username(self.payload.username)
        if not user:
            raise UnauthorizedException(message='Invalid credentials')

        if check_password_hash(user.password, self.payload.password):
            auth_payload = UserInListDto(
                id=user.id,
                username=user.username,
                role=user.role
            )
            expires_delta = timedelta(days=1)
            access_token = create_access_token(identity=auth_payload.dict(), expires_delta=expires_delta)
            refresh_token = create_refresh_token(identity=auth_payload.dict(), expires_delta=expires_delta)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "username": user.username,
                'role': user.role
            }
        else:
            raise UnauthorizedException(message="Invalid password")
