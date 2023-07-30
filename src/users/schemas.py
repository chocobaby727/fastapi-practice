from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str

    class Config:
        @staticmethod
        def schema_extra(schema: dict, _: type["CreateUserRequest"]):
            schema["example"] = {
                "email": "example@co.jp",
                "username": "テスト太郎",
                "first_name": "テスト",
                "last_name": "太郎",
                "password": "test1234",
                "role": "admin",
            }
