import pymongo
from injector import singleton, inject

from data.repository.mongo_client import AppMongoClient


class BaseRepository:
    @inject
    def __init__(self, client: AppMongoClient):
        self.client = client.client
        self.db = self.client.get_default_database()



