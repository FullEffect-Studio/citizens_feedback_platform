import csv
import json
import os

from flask import Blueprint, Response, request, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.application.dtos.save_feedback_dto import SaveFeedbackDto
from src.application.feedbacks.commands.process_feedback_command import ProcessFeedbackCommand
from src.application.feedbacks.queries.get_stats_by_social_worker_query import GetStatBySocialWorkerQuery
from src.application.feedbacks.queries.get_stats_public_official_query import GetStatsPublicOfficialQuery
from src.data.statistics.statistics_repository import StatisticsRepository
from src.domain.exceptions import HttpException, UnauthorizedException, BadRequestException
from src.domain.user import UserRole

blueprint = Blueprint('feedback', __name__)


@blueprint.route("/feedbacks/stats", methods=["Get"])
@jwt_required()
def get_stats(stats_repo: StatisticsRepository):
    current_user = get_jwt_identity()

    if current_user['role'] == UserRole.COMMUNITY_SOCIAL_WORKER:
        query = GetStatBySocialWorkerQuery(current_user_id=current_user['id'])
        result = query.execute(stats_repo=stats_repo)
        return Response(
            response=json.dumps(result.value),
            mimetype='application/json',
            status=200
        )
    elif current_user['role'] == UserRole.PUBLIC_OFFICIAL:
        query = GetStatsPublicOfficialQuery()
        result = query.execute(stats_repo=stats_repo)
        return Response(
            response=json.dumps(result.value),
            mimetype='application/json',
            status=200
        )
    else:
        raise UnauthorizedException()


@blueprint.route("/feedbacks/upload", methods=["POST"])
@jwt_required()
def upload_feedback(stats_repo: StatisticsRepository):
    current_user = get_jwt_identity()

    if current_user['role'] != UserRole.COMMUNITY_SOCIAL_WORKER:
        raise HttpException('Unauthorized access', 401)

    # Check if the request contains a file
    if "file" not in request.files:
        raise HttpException('csv file not found', 404)

    file = request.files["file"]

    # Check if the file is a CSV file
    if file.filename.split(".")[-1] != "csv":
        raise HttpException('Invalid file, must be a csv', 404)

    filepath = os.path.join(current_app.config['FILE_UPLOADS'], file.filename)
    file.save(filepath)
    feedback_data = []
    with open(filepath) as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            feedback_data.append(row)

    if feedback_data[0][0] != "what bothers you?" or feedback_data[0][1] != "age":
        raise BadRequestException('The first column header of the csv must contain "what bothers you?" and the second '
                            'column header should be "age"')

    # Check for errors int errors in data points
    data_points = feedback_data[1:]
    for data in data_points:
        try:
            if data[1].isdigit():
                x = int(data[1])
        except ValueError as e:
            print(e)
            raise BadRequestException('values in age column must be integers')

    for i in range(0, len(feedback_data)):
        if i > 0:
            feedback_data[i][1] = int(feedback_data[i][1])

    print(feedback_data)
    # Check if the community name and size are provided
    community_name = request.form.get("community_name")
    community_size = request.form.get("community_size")
    if not community_name or not community_size:
        raise BadRequestException('Community name and community size are required')

    # Validate the community size
    try:
        community_size = int(community_size)
    except ValueError:
        raise BadRequestException('Community size must be an integer')

    payload = SaveFeedbackDto(feedback=feedback_data[1:], community_name=community_name, community_size=community_size)

    command = ProcessFeedbackCommand(payload=payload, current_user_id=current_user['id'])
    command.execute(stats_repo=stats_repo)

    os.remove(filepath)

    return Response(response=None, mimetype='application/json', status=200)
