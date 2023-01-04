import json

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, create_access_token
from marshmallow import ValidationError

from src.application.dtos.login_credentials_dto import LoginCredentialsDtoSchema
from src.application.users.commands.login_user_command import LoginUserCommand
from src.data.users.users_repository import UsersRepository
from src.domain.exceptions import BadRequestException

blueprint = Blueprint('auth', __name__)

# CORS(blueprint)


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
        raise BadRequestException(message=e.messages)


@blueprint.route("/auth/refresh", methods=["POST"])
def refresh_api_route():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return {"access_token": access_token}, 200


