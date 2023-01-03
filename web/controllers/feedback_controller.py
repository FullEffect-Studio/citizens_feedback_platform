import csv
import json
import os

import chardet
from flask import Blueprint, Response, request, current_app
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from marshmallow import ValidationError

from application.dtos.login_credentials_dto import LoginCredentialsDtoSchema
from application.dtos.save_feedback_dto import SaveFeedbackDto
from application.dtos.user_list_dto import UserInListDto
from application.feedbacks.commands.save_feedback_command import SaveFeedbackCommand
from application.users.commands.login_user_command import LoginUserCommand
from data.statistics.statistics_repository import StatisticsRepository
from data.users.users_repository import UsersRepository
from domain.exceptions.invalid_user_input_exception import HttpException
from domain.user import UserRole

blueprint = Blueprint('feedback', __name__)


@blueprint.route("/feedbacks/upload", methods=["POST"])
@jwt_required()
def upload_feedback(stats_repo: StatisticsRepository):
    current_user = get_jwt_identity()

    # Check if the user has the "community_social_worker" role
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
        raise HttpException('The first column header of the csv must contain "what bothers you?" and the second '
                            'column header should be "age"', 401)

    # Check for errors int errors in data points
    data_points = feedback_data[1:]
    for data in data_points:
        try:
            if data[1].isdigit():
                x = int(data[1])
        except ValueError as e:
            print(e)
            raise HttpException('values in age column must be integers', 401)

    for i in range(0, len(feedback_data)):
        if i > 0:
            feedback_data[i][1] = int(feedback_data[i][1])

    print(feedback_data)
    # Check if the community name and size are provided
    community_name = request.form.get("community_name")
    community_size = request.form.get("community_size")
    if not community_name or not community_size:
        raise HttpException('Community name and community size are required', 401)

    # Validate the community size
    try:
        int(community_size)
    except ValueError:
        raise HttpException('Community size must be an integer', 404)

    payload = SaveFeedbackDto(feedback=feedback_data[1:], community_name=community_name, community_size=community_size)

    command = SaveFeedbackCommand(payload=payload, current_user_id=current_user['id'])
    command.execute(stats_repo=stats_repo)

    return [feedback_data[1:], community_name, community_size]  # return redirect(url_for("upload_feedback"))
