import json

from flask import Blueprint, Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from injector import inject
from marshmallow import ValidationError

from cfp.application.messages.commands.revise_data_command import ReviseDataCommand
from cfp.application.messages.queries.get_messages_social_worker_query import GetMessagesForSocialWorkerQuery
from cfp.data.messages.messages_repository import MessagesRepository
from cfp.domain.common.exceptions import UnauthorizedException, BadRequestException
from cfp.domain.dtos.revise_data_dto import ReviseDataDtoSchema
from cfp.domain.values.user_role import UserRole

blueprint = Blueprint('messages', __name__)


@blueprint.route("/messages", methods=["GET"])
@jwt_required()
@inject
def get_messages(msg_repo: MessagesRepository):
    current_user = get_jwt_identity()
    if current_user['role'] != UserRole.COMMUNITY_SOCIAL_WORKER:
        raise UnauthorizedException()

    query = GetMessagesForSocialWorkerQuery(current_user_id=current_user['id'])
    result = query.execute(msg_repo=msg_repo)

    return Response(
        json.dumps(result.value),
        mimetype='application/json',
        status=200
    )


@blueprint.route("/messages", methods=["POST"])
@inject
def revise_data(msg_repo: MessagesRepository):

    current_user = get_jwt_identity()
    if current_user['role'] != UserRole.PUBLIC_OFFICIAL:
        raise UnauthorizedException()

    schema = ReviseDataDtoSchema()
    try:
        data = schema.load(request.get_json())
        command = ReviseDataCommand(payload=data)
        command.execute(msg_repo)

        return Response(None, mimetype='application/json', status=201)
    except ValidationError as e:
        print(e)
        raise BadRequestException(message=e.messages)

