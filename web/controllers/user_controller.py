import json

from flask import Blueprint, Response, request
from injector import inject
from marshmallow import ValidationError

from application.users.commands.add_user_command import AddUserCommand
from data.repository.users_repository import UsersRepository
from domain.serializers.user import UserJsonEncoder
from domain.usecases.user_list import user_list_usecase
from web.controllers.add_user_dto import AddUserDtoSchema
from web.http_status_codes import STATUS_CODES

blueprint = Blueprint('user', __name__)


@blueprint.route("/users", methods=["GET"])
@inject
def user_list(user_repo: UsersRepository):
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
        user_id = command.execute(user_repo)

        return Response(None, mimetype='application/json', status=201)
    except ValidationError as e:
        print(e)
        return Response(e.messages)

    # return Response(
    #     json.dumps(result.value, cls=UserJsonEncoder),
    #     mimetype='application/json',
    #     status=STATUS_CODES[result.type]
    # )
