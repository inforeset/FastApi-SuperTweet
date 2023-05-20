from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.model.likes import Like
from app.model.tweets import Tweet
from app.schemas.base_schema import BaseSchema
from app.schemas.tweet_schema import TweetIn, TweetOut, TweetsOut
from app.schemas.user_schema import User
from app.utils.authentication import get_current_user
from app.utils.database import get_session
from app.utils.settings import (
    RESPONSE_401_422,
    RESPONSE_401_422_404,
    RESPONSE_401_422_404_403,
)
from app.utils.utils import bind_media_to_tweet, get_like, get_tweet, get_tweets

router = APIRouter()


@router.post(
    "/tweets", response_model=TweetOut, responses=RESPONSE_401_422, status_code=201
)
async def create_tweet(
    tweet: TweetIn,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    """Создать твит"""
    new_tweet = Tweet(tweet_data=tweet.tweet_data, user_id=current_user.id)
    session.add(new_tweet)
    await session.flush()
    ids: list = tweet.tweet_media_ids
    if ids:
        await bind_media_to_tweet(session, ids, new_tweet.id)
    await session.commit()
    return new_tweet


@router.delete(
    "/tweets/{id}",
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404_403,
    status_code=200,
)
async def delete_tweet(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    """Удалить твит"""
    tweet = await get_tweet(id, session)
    if tweet.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden",
        )
    await session.delete(tweet)
    await session.commit()
    return tweet


@router.post(
    "/tweets/{id}/likes",
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404,
    status_code=200,
)
async def add_like(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    """Поставить лайк"""
    tweet = await get_tweet(id, session)
    if not await get_like(session=session, user_id=current_user.id, tweet_id=tweet.id):
        like = Like(user_id=current_user.id, tweets_id=tweet.id)
        session.add(like)
        await session.commit()
    return "OK"


@router.delete(
    "/tweets/{id}/likes",
    response_model=BaseSchema,
    responses=RESPONSE_401_422_404,
    status_code=200,
)
async def delete_like(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    """Удалить лайк"""
    tweet = await get_tweet(id, session)
    like = await get_like(session=session, user_id=current_user.id, tweet_id=tweet.id)
    if like:
        await session.delete(like)
        await session.commit()
    return "OK"


@router.get("/tweets", response_model=TweetsOut, status_code=200)
async def get_all_tweets(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    """Получить все твиты для ленты пользователя"""
    tweets = await get_tweets(session, current_user)

    return {"tweets": tweets}
