import json

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from injector import inject
from marshmallow import ValidationError

from application.users.commands.add_user_command import AddUserCommand
from data.users.users_repository import UsersRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from domain.serializers.user import UserJsonEncoder
from domain.usecases.user_list import user_list_usecase
from application.dtos.add_user_dto import AddUserDtoSchema
from web.http_status_codes import STATUS_CODES

blueprint = Blueprint('user', __name__)


@blueprint.route("/users", methods=["GET"])
@jwt_required()
@inject
def user_list(user_repo: UsersRepository):

    current_user = get_jwt_identity()
    # print(f"Hello, {current_user}!")

    result = user_list_usecase(user_repo)

    return Response(
        json.dumps(result.value, cls=UserJsonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[result.type]
    )


@blueprint.route("/users", methods=["POST"])
@inject
def add_user(user_repo: UsersRepository):
    schema = AddUserDtoSchema()
    try:
        data = schema.load(request.get_json())
        command = AddUserCommand(payload=data)
        response = command.execute(user_repo)

        return Response(None, mimetype='application/json', status=201)
    except ValidationError as e:
        print(e)
        raise HttpException(message=e.messages, status_code=400)

