import pprint
from typing import List
from injector import inject

from data.messages.messages_data import MessageData
from data.mongo_base import BaseRepository, AppMongoClient
from data.statistics.statistics_data import StatisticData
from domain.message import Message
from domain.statistic import Statistic


class MessagesRepository(BaseRepository):
    @inject
    def __init__(self, client: AppMongoClient):
        super().__init__(client)
        self.messages = self.client.get_default_database().get_collection('messages')

    def get_messages(self, social_worker_id):
        try:
            result = self.messages.find({'social_worker_id': social_worker_id})
            return [self._build_message(data) for data in result]
        except Exception as e:
            print(e)
            raise e

    def save_message(self, domain_msg: Message):
        data = domain_msg.to_dict()
        data['id'] = str(domain_msg.id)
        # pprint.pprint(data)

        try:
            model = MessageData(**data).save()
        except Exception as e:
            print(e)
            raise e

    def _build_message(self, result):
        return Message(
            id=result['_id'],
            community_name=result['community_name'],
            social_worker_id=result['social_worker_id'],
            date_created=result['date_created'],

        )
