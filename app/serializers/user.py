import json

from app.domain.user import User


class UserJsonEncoder(json.JSONEncoder):
    def default(self, o: User):
        try:
            to_serialize = {
                "id": str(o.id),
                "username": o.username,
                "password": o.password
            }
            print('serializer return type', type(to_serialize))
            return to_serialize
        except AttributeError:  # pragma: no cover
            return super().default(0)
