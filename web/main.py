# main.py
from flask import Flask, request
from controllers.user_controller import UserController
from web.repositories.user_repository import UserRepository
from web.services.user_service import UserService

app = Flask(__name__)

user_repository = UserRepository()
user_service = UserService(repository=user_repository)
user_controller = UserController(user_service=user_service)


@app.route("/users", methods=["GET"])
def get_users():
    return UserController(user_service=user_service).get_all()
