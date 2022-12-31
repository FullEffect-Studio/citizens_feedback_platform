import json
from uuid import uuid4

from app.domain.user import User, UserRole
from app.serializers.user import UserJsonEncoder
from pprint import pprint as pp


def test_serialize_domain_user():
    code = uuid4()
    user = User(
        id=code,
        username='Ben',
        password='qwe123!',
        role=UserRole.COMMUNITY_SOCIAL_WORKER
    )

    expected_json = f"""
        {{
            "id": "{code}",
            "username": "Ben",
            "password": "qwe123!",
            "role": "{UserRole.COMMUNITY_SOCIAL_WORKER.value}"
        }}
    """

    json_room = json.dumps(user, cls=UserJsonEncoder)
    assert json.loads(json_room) == json.loads(expected_json)

