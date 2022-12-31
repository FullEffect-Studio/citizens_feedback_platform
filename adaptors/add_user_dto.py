from pydantic import BaseModel


class AddUserDto(BaseModel):
    name: str
    age: int
