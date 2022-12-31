# main.py
from flask import Flask, request, jsonify
from pydantic import ValidationError

from web.controllers.user_controller import UserController
from web.adaptors.add_user_dto import AddUserDto
from web.repositories.user_repository import UserRepository
from web.services.user_service import UserService

app = Flask(__name__)

user_repository = UserRepository()
user_service = UserService(repository=user_repository)
user_controller = UserController(user_service=user_service)


@app.route("/users", methods=["GET"])
def get_users():
    return user_controller.get_all()


@app.route('/users', methods=['POST'])
def add_user():

    try:
        payload = AddUserDto(**request.get_json())
        return jsonify({
            'message': 'Successful',
            'data': {
                'name': payload.name,
                'age': payload.age
            }
        })
    except ValidationError as e:
        print(e)
        return jsonify({
            'message': 'Invalid payload',
            'data': e.errors()
        })


