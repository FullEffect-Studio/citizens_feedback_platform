import pymongo
from injector import singleton


@singleton
class AppMongoClient:
    def __init__(self, client: pymongo.MongoClient):
        self.client = client
