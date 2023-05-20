from pydantic import BaseModel


class BaseSchema(BaseModel):
    result: bool = True

    class Config:
        orm_mode = True
