from marshmallow import Schema, fields, post_load
from pydantic import BaseModel


class AddUserDto(BaseModel):
    username: str
    role: str
    password: str


class AddUserDtoSchema(Schema):
    username = fields.Str()
    role = fields.Str()
    password = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return AddUserDto(**data)


