from pydantic import BaseModel


class UserListDto(BaseModel):
    id: str
    username: str
    role: str

