from marshmallow import Schema, fields, post_load
from pydantic import BaseModel


class LoginCredentialsDto(BaseModel):
    username: str
    password: str


class LoginCredentialsDtoSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make(self, data, **kwargs):
        return LoginCredentialsDto(**data)


