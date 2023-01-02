import json

from flask import Blueprint, Response, request
from marshmallow import fields, Schema, ValidationError

from application.dtos.login_credentials_dto import LoginCredentialsDtoSchema, LoginCredentialsDto
from application.users.commands.login_user_command import LoginUserCommand
from data.repository.users_repository import UsersRepository
from domain.exceptions.invalid_user_input_exception import HttpException

blueprint = Blueprint('auth', __name__)


@blueprint.route("/auth/login", methods=["POST"])
def login(user_repo: UsersRepository):
    schema = LoginCredentialsDtoSchema()

    try:
        data = schema.load(request.get_json())
        command = LoginUserCommand(payload=data)
        response = command.execute(user_repo)
        print(response)
        return Response(json.dumps(response), mimetype='application/json', status=201)
    except ValidationError as e:
        print(e.messages)
        raise HttpException(message=e.messages, status_code=400)

