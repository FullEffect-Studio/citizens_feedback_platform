import pymongo
from flask import Flask
from flask_injector import FlaskInjector
from injector import provider, Module, singleton, Injector, inject, Binder

from application.command_bus import CommandBus
from application.command_handler import CommandHandler
from data.repository.mongo_client import AppMongoClient
from web.db_seeder import db_seeder
from web.controllers import user_controller, auth_controller


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


def create_app(config_name):
    app = Flask(__name__)

    config_module = f"web.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    configure_blueprints(app)

    print('Connecting db: ', app.config['MONGODB_URL'])
    print('JWT_SECRET_KEY: ', app.config['JWT_SECRET_KEY'])
    db_seeder(app.config['MONGODB_URL'])

    FlaskInjector(app=app, modules=[MongoModule(app=app)])

    return app


def configure_blueprints(app):
    app.register_blueprint(user_controller.blueprint)
    app.register_blueprint(auth_controller.blueprint)
