import json

from flask import Blueprint, Response, request

from app.repository.memrepo import MemRepo
from app.requests.user_list import build_user_list_request
from app.responses import ResponseTypes
from app.serializers.user import UserJsonEncoder
from app.usecases.user_list import user_list_usecase

blueprint = Blueprint('user', __name__)

STATUS_CODES = {
    ResponseTypes.SUCCESS: 200,
    ResponseTypes.RESOURCE_ERROR: 404,
    ResponseTypes.PARAMETERS_ERROR: 400,
    ResponseTypes.SYSTEM_ERROR: 500,
}

users = [
    {
        "id": "f853578c-fc0f-4e65-81b8-566c5dffa35a",
        "username": "Danquah",
        "password": "pass111",
        "role": 'Administrator'
    },
    {
        "id": "fe2c3195-aeff-487a-a08f-e0bdc0ec6e9a",
        "username": "Fahrid",
        "password": "pass222",
        "role": 'Administrator'
    },
    {
        "id": "913694c6-435a-4366-ba0d-da5334a611b2",
        "username": "Yau",
        "password": "pass333",
        "role": 'Administrator'
    },

    {
        "id": "913694c6-435a-4366-ba0d-da5334a611b2",
        "username": "Lowe",
        "password": "pass444",
        "role": 'Administrator'
    },
]


@blueprint.route("/users", methods=["GET"])
def user_list():
    request_object = {
        "filters": {}
    }
    querystring_params = {
        "filters": {}
    }

    for arg, values in request.args.items():
        if arg.startswith('filter_'):
            querystring_params['filters'][arg.replace('filter_', '')] = values

        request_object = build_user_list_request(filters=querystring_params['filters'])

    repo = MemRepo(users)
    result = user_list_usecase(repo, request_object)

    return Response(
        json.dumps(result.value, cls=UserJsonEncoder),
        mimetype='application/json',
        status=STATUS_CODES[result.type]
    )
