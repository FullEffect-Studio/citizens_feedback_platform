import uuid
from dataclasses import dataclass,asdict


@dataclass
class User:
    id: uuid.UUID
    username: str
    password: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)
