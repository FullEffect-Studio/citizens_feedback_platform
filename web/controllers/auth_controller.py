from flask import Blueprint, Response, request
from marshmallow import fields, Schema, ValidationError

from application.dtos.login_dto import LoginDto
from data.repository.users_repository import UsersRepository

blueprint = Blueprint('auth', __name__)


class LoginDtoSchema(Schema):
    username = fields.Str()
    password = fields.Str()


@blueprint.route("/auth/login", methods=["POST"])
def login(user_repo: UsersRepository):
    schema = LoginDtoSchema()

    try:
        data = schema.load(request.get_json())
        print('validation results', data, type(request.get_json()))
        payload = LoginDto(**data)
        print(payload)
        return Response(schema.dumps(data))
    except ValidationError as e:
        print(e)
        return Response(e.messages)

    # repo = MongoRepo(uri=current_app.config['MONGODB_URL'], db_name='')
    # result = user_list_usecase(repo)

    # return Response(
    #     json.dumps(payload.dict(), cls=UserJsonEncoder),
    #     mimetype='application/json',
    #     status=201
    # )
