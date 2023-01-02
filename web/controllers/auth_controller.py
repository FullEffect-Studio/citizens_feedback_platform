import json

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, create_access_token
from marshmallow import ValidationError

from application.dtos.login_credentials_dto import LoginCredentialsDtoSchema
from application.users.commands.login_user_command import LoginUserCommand
from data.users.users_repository import UsersRepository
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


@blueprint.route("/auth/refresh", methods=["POST"])
def refresh_api_route():
    # Get the current user's identity from the refresh token
    current_user = get_jwt_identity()

    # Create a new access token for the user
    access_token = create_access_token(identity=current_user)

    # Return the new access token to the user
    return {"access_token": access_token}, 200


