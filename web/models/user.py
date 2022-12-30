# models/user.py
from mongoengine import Document, StringField, IntField


class User(Document):
    name = StringField(required=True)
    age = IntField(required=True)
