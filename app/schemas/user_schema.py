from pydantic import BaseModel

from .base_schema import BaseSchema


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class BaseUser(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class User(BaseUser):
    following: list[BaseUser]
    followers: list[BaseUser]

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True


class UserOut(BaseSchema):
    user: User
