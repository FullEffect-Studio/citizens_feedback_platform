from data.mongo_base import BaseRepository, AppMongoClient


class FeedBacksRepository(BaseRepository):
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.feedbacks = self.client.get_default_database().get_collection('users')

    def list(self):
        result = self.feedbacks.find()
        return [
            q
            for q in result
        ]
