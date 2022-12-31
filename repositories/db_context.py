from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:fulleffect@cluster0.b7xsp.mongodb.net/cfp_dev_db?retryWrites=true&w=majority")


class MongoDbContext:
    def __init__(self):
        self.client = client
        self.db = self.client.get_database('cfp_dev_db')
