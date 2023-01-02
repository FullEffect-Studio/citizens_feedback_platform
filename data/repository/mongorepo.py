import pymongo

from domain.user import User


class MongoRepo:
    def __init__(self, uri, db_name):
        client = pymongo.MongoClient(uri)
        self.db = client.get_default_database()

    def list(self):
        collection = self.db.users

        result = collection.find()
        return [
            User(
                id=q['id'],
                username=q['username'],
                password=q['password'],
                role=q['role']
            )
            for q in result
        ]
