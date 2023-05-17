from typing import Optional, Any

from pydantic import BaseModel, Field, root_validator
from pydantic.utils import GetterDict

from .base_schema import BaseSchema
from .user_schema import BaseUser


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[list[int]]


class TweetOut(BaseSchema):
    id: int = Field(alias="tweet_id")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Like(BaseModel):
    id: int = Field(alias='user_id')
    username: str = Field(alias='name')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def extract_username(cls, v):
        return vars(v['user'])


class TweetGetter(GetterDict):

    def get(self, key: str, default: Any = None) -> Any:
        if key == 'attachments':
            medias = [
                *[x.path_media for x in self._obj.medias],
            ]
            return medias

        else:
            return super(TweetGetter, self).get(key, default)


class TweetOutAll(BaseModel):
    id: int
    tweet_data: str = Field(alias="content")
    user: BaseUser = Field(alias="author")
    likes: list[Like]
    attachments: list

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        getter_dict = TweetGetter


class TweetsOut(BaseSchema):
    tweets: list[TweetOutAll]
