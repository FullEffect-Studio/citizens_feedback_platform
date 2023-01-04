import json

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from injector import inject
from marshmallow import ValidationError

from application.users.commands.add_user_command import AddUserCommand
from application.users.queries.get_all_users_query import GetAllUsersQuery
from data.users.users_repository import UsersRepository
from domain.exceptions import  UnauthorizedException, BadRequestException
from application.dtos.add_user_dto import AddUserDtoSchema
from domain.user import UserRole

blueprint = Blueprint('user', __name__)


@blueprint.route("/users", methods=["GET"])
@jwt_required()
@inject
def user_list(users_repo: UsersRepository):

    current_user = get_jwt_identity()
    if current_user['role'] != UserRole.ADMIN:
        raise UnauthorizedException()

    query = GetAllUsersQuery()
    result = query.execute(users_repo=users_repo)

    return Response(
        json.dumps(result.value),
        mimetype='application/json',
        status=200
    )


@blueprint.route("/users", methods=["POST"])
@inject
def add_user(user_repo: UsersRepository):
    schema = AddUserDtoSchema()
    try:
        data = schema.load(request.get_json())
        command = AddUserCommand(payload=data)
        command.execute(user_repo)

        return Response(None, mimetype='application/json', status=201)
    except ValidationError as e:
        print(e)
        raise BadRequestException(message=e.messages)

