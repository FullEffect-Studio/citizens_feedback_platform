import uuid

from mongoengine import Document, StringField, ListField, IntField, UUIDField


class StatisticData(Document):
    id = StringField(primary_key=True, default=str(uuid.uuid4()))
    community_name = StringField(required=True, unique=True)
    community_size = IntField(required=True, default=0)
    social_worker_id = StringField(required=True)
    family = IntField(required=True, default=0)
    health = IntField(required=True, default=0)
    unknown = IntField(required=True, default=0)

    meta = {'collection': 'statistics'}


