import uuid

from mongoengine import Document, StringField, UUIDField


class UserData(Document):
    id = StringField(primary_key=True, default=str(uuid.uuid4()))
    username = StringField(required=True, unique=True)
    password = StringField(required=True)
    role = StringField(required=True)

    meta = {'collection': 'users'}

