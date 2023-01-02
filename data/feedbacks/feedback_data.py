from mongoengine import Document, StringField, ListField, UUIDField


class Feedback(Document):
    _id = UUIDField(binary=False, required=True, default=uuid.uuid4)
    topic = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    location = StringField(required=True)
    status = StringField(default="pending")
    comments = ListField(StringField())
