import uuid
from dataclasses import dataclass, asdict
from enum import Enum
from sqlite3 import Date


@dataclass
class Message:
    id: uuid.UUID
    social_worker_id: str
    community_name: str
    date_created: Date


    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)


