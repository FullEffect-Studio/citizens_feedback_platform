# controllers/user_controller.py
from flask import jsonify


class UserController:

    def __init__(self, user_service):
        self.user_service = user_service

    def get_all(self):
        users = self.user_service.get_all()
        return jsonify([user.to_json() for user in users])

    def create(self, data):
        user = self.user_service.create(data)
        return jsonify(user.to_json()), 201
