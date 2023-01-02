from pydantic import BaseModel


class LoginDto(BaseModel):
    username: str
    password: str

    @classmethod
    def rules(cls):
        return {
            "username": "required|min:3",
            "password": "required|min:6",
        }


