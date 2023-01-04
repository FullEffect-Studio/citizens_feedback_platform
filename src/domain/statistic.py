import uuid
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class Statistic:
    id: uuid.UUID
    community_name: str
    community_size: int
    social_worker_id: str
    family: int
    health: int
    unknown: int

    def get_family_percent(self) -> float:
        return round((self.family / self._get_total()) * 100, 2)

    def get_health_percent(self) -> float:
        return round((self.health / self._get_total()) * 100, 2)

    def get_unknown_percent(self) -> float:
        return round((self.family / self._get_total()) * 100, 2)

    def _get_total(self):
        return self.family + self.health + self.unknown

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return f"<Statistic>" \
               f"id: {str(self.id)}" \
               f"family: {self.family}" \
               f"health: {self.health}" \
               f"unknown:{self.unknown}"
