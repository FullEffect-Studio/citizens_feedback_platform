from marshmallow import Schema, fields, post_load
from pydantic import BaseModel


class ReviseDataDto(BaseModel):
    community_name: str
    social_worker_id: str


class ReviseDataDtoSchema(Schema):
    community_name = fields.Str()
    social_worker_id = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return ReviseDataDto(**data)


