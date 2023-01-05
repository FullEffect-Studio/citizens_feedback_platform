import os
import sys
from logging import config

from flask import Flask, make_response, jsonify
import logging
from logging.config import fileConfig, dictConfig
from flask_cors import CORS
from flask_injector import FlaskInjector
from flask_jwt_extended import JWTManager
from marshmallow import ValidationError
from mongoengine import connect

from cfp.domain.common.exceptions import UnauthorizedException, HttpException, BadRequestException
from cfp.web.controllers import users_controller, auth_controller, feedback_controller, messages_controller
from cfp.data.db_seeder import db_seeder
from cfp.web.modules.mongo_module import MongoModule


def create_app(config_name):
    app = Flask(__name__)

    config_module = f"cfp.web.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    logger = configure_logging(app)
    configure_blueprints(app)

    logger.info(f'Executing app in {config_name} environment')

    # Configure database clients
    db_seeder(app.config['MONGODB_URL'])
    connect(host=app.config['MONGODB_URL'])
    logger.info(f'Connecting to mongodb at {app.config["MONGODB_URL"]}')
    logger.info(f'MongoEngine connected to cluster')

    FlaskInjector(app=app, modules=[MongoModule(app=app)])

    jwt = JWTManager(app)
    CORS(app)

    # Error handling middlewares
    @app.errorhandler(Exception)
    def handle_error(error):
        logger.exception('[Exception]' + str(error))
        return make_response(jsonify({'error': str(error)}), 500)

    @app.errorhandler(HttpException)
    def handle_error(error: HttpException):
        logger.exception('[HttpException]' + str(error.message), error.status_code)
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(UnauthorizedException)
    def handle_error(error: HttpException):
        logger.exception('[UnauthorizedException]' + str(error.message), error.status_code)
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(BadRequestException)
    def handle_error(error: HttpException):
        logger.exception('[BadRequestException]' + str(error.message), error.status_code)
        return make_response(jsonify({'error': str(error.message)}), error.status_code)

    @app.errorhandler(ValidationError)
    def handle_error(error: ValidationError):
        logger.exception('[ValidationError]' + str(error.messages), 400)
        return make_response(jsonify({'error': str(error.messages)}), 400)

    return app


def configure_logging(app):
    config.dictConfig(app.config['LOGGING'])
    logger = logging.getLogger(__name__)
    return logger


def configure_blueprints(app):
    app.register_blueprint(users_controller.blueprint)
    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(feedback_controller.blueprint)
    app.register_blueprint(messages_controller.blueprint)
