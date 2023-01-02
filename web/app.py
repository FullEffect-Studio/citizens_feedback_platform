import pymongo
from flask import Flask, make_response, jsonify
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from injector import Module, singleton, inject, Binder
from marshmallow import ValidationError
from mongoengine import connect

from application.command_bus import CommandBus
from data.mongo_client import AppMongoClient
from domain.exceptions.invalid_user_input_exception import HttpException
from web.db_seeder import db_seeder
from web.controllers import user_controller, auth_controller, feedback_controller


class MongoModule(Module):

    def __init__(self, app: Flask):
        self.app = app

    @inject
    def configure(self, binder):
        mongo_url = self.app.config['MONGODB_URL'],
        mongo_client = pymongo.MongoClient(mongo_url)

        binder.bind(
            pymongo.MongoClient,
            mongo_client,
            scope=singleton)

        binder.bind(AppMongoClient, AppMongoClient(client=mongo_client))


class CqrsModule(Module):

    @inject
    def configure(self, binder: Binder):
        binder.bind(CommandBus, CommandBus())



class CFPFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, dict):
            return make_response(jsonify({'result': rv}), 200)
        if isinstance(rv, tuple) and len(rv) == 2 and isinstance(rv[0], dict) and isinstance(rv[1], int):
            return make_response(jsonify(rv[0]), rv[1])
        return Flask.make_response(self, rv)


def create_app(config_name):
    app = CFPFlask(__name__)

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

    @app.errorhandler(Exception)
    def handle_error(error):
        return make_response(jsonify({'error': str(error)}), 500)

    @app.errorhandler(HttpException)
    def handle_error(error: HttpException):
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(ValidationError)
    def handle_error(error: ValidationError):
        return make_response(jsonify({'error': str(error.messages)}), 400)

    return app


def configure_blueprints(app):
    app.register_blueprint(user_controller.blueprint)
    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(feedback_controller.blueprint)

