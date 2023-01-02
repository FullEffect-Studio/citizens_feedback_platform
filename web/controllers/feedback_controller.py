import csv
import json

from flask import Blueprint, Response, request
from flask_jwt_extended import get_jwt_identity, create_access_token
from marshmallow import ValidationError

from application.dtos.login_credentials_dto import LoginCredentialsDtoSchema
from application.users.commands.login_user_command import LoginUserCommand
from data.users.users_repository import UsersRepository
from domain.exceptions.invalid_user_input_exception import HttpException

blueprint = Blueprint('feedback', __name__)


@blueprint.route("/feedbacks/upload", methods=["POST"])
def upload_feedback():
    current_user = get_jwt_identity()

    # Check if the user has the "community_social_worker" role
    if current_user.role != "community_social_worker":
        raise HttpException('Unauthorized access', 401)

    # Check if the request contains a file
    if "file" not in request.files:
        raise HttpException('csv file not found', 404)

    file = request.files["file"]

    # Check if the file is a CSV file
    if file.filename.split(".")[-1] != "csv":
        raise HttpException('Invalid file, must be a csv', 404)

    # Read the CSV file and parse the feedback data
    feedback_data = []
    reader = csv.reader(file)
    for i, row in enumerate(reader):
        # Validate the CSV format
        if i == 0:
            if row[0] != "what bothers you?" or row[1] != "age":
                raise HttpException('The first row header of the csv must contain "what bothers you?" and the second '
                                    'row header should be "age"', 401)

        else:
            # Validate the data types
            try:
                int(row[1])
            except ValueError:
                raise HttpException('values in age column must be integers', 401)
            feedback_data.append(row)

    # Check if the community name and size are provided
    community_name = request.form.get("community_name")
    community_size = request.form.get("community_size")
    if not community_name or not community_size:
        raise HttpException('Community name and community size are required', 401)

    # Validate the community size
    try:
        int(community_size)
    except ValueError:
        return HttpException('Community size must be an integer', 404)

    # Save the feedback data to the database
    # save_feedback_data(feedback_data, community_name, community_size)

    return feedback_data, community_name, community_size
    # return redirect(url_for("upload_feedback"))




