from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from mongoengine import connect

from src.domain.exceptions import HttpException, UnauthorizedException, BadRequestException
from src.web.database.db_seeder import db_seeder
from src.web.controllers import users_controller, auth_controller, feedback_controller, messages_controller
from src.web.database.mongo_module import MongoModule


def create_app(config_name):
    app = Flask(__name__)

    config_module = f"web.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    configure_blueprints(app)

    print('Connecting db: ', app.config['MONGODB_URL'])
    print('JWT_SECRET_KEY: ', app.config['JWT_SECRET_KEY'])
    db_seeder(app.config['MONGODB_URL'])

    # Connecting mongo-engine
    connect(host=app.config['MONGODB_URL'])

    FlaskInjector(app=app, modules=[MongoModule(app=app)])

    jwt = JWTManager(app)
    CORS(app)
    # cors = CORS(app, resources={r"/*": {"origins": "*"}})

    @app.errorhandler(Exception)
    def handle_error(error):
        return make_response(jsonify({'error': str(error)}), 500)

    @app.errorhandler(HttpException)
    def handle_error(error: HttpException):
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(UnauthorizedException)
    def handle_error(error: HttpException):
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(BadRequestException)
    def handle_error(error: HttpException):
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(ValidationError)
    def handle_error(error: ValidationError):
        return make_response(jsonify({'error': str(error.messages)}), 400)

    return app


def configure_blueprints(app):
    app.register_blueprint(users_controller.blueprint)
    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(feedback_controller.blueprint)
    app.register_blueprint(messages_controller.blueprint)
