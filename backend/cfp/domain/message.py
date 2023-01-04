import datetime
import uuid
from dataclasses import dataclass, asdict


@dataclass
class Message:
    id: uuid.UUID
    social_worker_id: str
    community_name: str
    date_created: datetime.datetime.date

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)
