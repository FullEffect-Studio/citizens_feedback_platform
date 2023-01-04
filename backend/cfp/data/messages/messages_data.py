import uuid
from datetime import datetime

from mongoengine import Document, StringField, DateTimeField


class MessageData(Document):
    id = StringField(primary_key=True, default=str(uuid.uuid4()))
    community_name = StringField(required=True)
    social_worker_id = StringField(required=True)
    date_created = DateTimeField(required=True, default=datetime.now)

    meta = {'collection': 'messages'}
