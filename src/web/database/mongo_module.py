import pymongo
from flask import Flask
from injector import Module, inject, singleton

from src.data.messages.messages_repository import MessagesRepository
from src.data.mongo_client import AppMongoClient
from src.data.statistics.statistics_repository import StatisticsRepository
from src.data.users.users_repository import UsersRepository


class MongoModule(Module):

    def __init__(self, app: Flask):
        self.app = app

    @inject
    def configure(self, binder):
        mongo_url = self.app.config['MONGODB_URL'],
        mongo_client = pymongo.MongoClient(mongo_url)
        app_mongo_client = AppMongoClient(client=mongo_client)

        binder.bind(
            pymongo.MongoClient,
            mongo_client,
            scope=singleton)

        binder.bind(AppMongoClient, app_mongo_client)
        binder.bind(UsersRepository, UsersRepository(client=app_mongo_client))
        binder.bind(StatisticsRepository, StatisticsRepository(client=app_mongo_client))
        binder.bind(MessagesRepository, MessagesRepository(client=app_mongo_client))

