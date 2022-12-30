from flask_restful import Resource


class UsersController(Resource):
    def get(self):
        return 'all users'
