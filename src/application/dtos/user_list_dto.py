from dataclasses import dataclass, asdict

from pydantic import BaseModel


@dataclass()
class UserInListDto:
    id: str
    username: str
    role: str

    def dict(self):
        return asdict(self)
