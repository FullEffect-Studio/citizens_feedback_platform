import uuid
from dataclasses import dataclass, asdict
from enum import Enum


class UserRole:
    COMMUNITY_SOCIAL_WORKER = 'Social Worker'
    PUBLIC_OFFICIAL = 'Public Official'
    ADMIN = 'Administrator'


@dataclass
class User:
    id: uuid.UUID
    username: str
    password: str
    role: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)
