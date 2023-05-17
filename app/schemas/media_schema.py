from pydantic import Field

from .base_schema import BaseSchema


class MediaOut(BaseSchema):
    id: int = Field(alias="media_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
