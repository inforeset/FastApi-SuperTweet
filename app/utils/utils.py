from contextlib import suppress
from pathlib import Path
import aiofiles
from fastapi import UploadFile, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.model.likes import Like
from app.model.media import Media
from app.model.tweets import Tweet
from app.model.users import User
from app.utils.settings import MEDIA_ROOT


async def prepare_media_dir() -> None:
    Path(MEDIA_ROOT).mkdir(mode=0o777, parents=False, exist_ok=True)


async def get_filename(path: Path) -> Path:
    counter = 0
    dir = path.resolve().parent
    file = path.stem
    extension = path.suffix
    if path.exists():
        while Path(str(dir), f'{file} ({counter}){extension}').is_file():
            counter += 1
        return Path(str(dir), f'{file} ({counter}){extension}')
    return path


async def write_file(file: UploadFile) -> str:
    with suppress(OSError):
        await prepare_media_dir()
        path = Path(MEDIA_ROOT, file.filename)
        filename = await get_filename(path)
        contents = file.file.read()
        async with aiofiles.open(filename, mode='wb') as f:
            await f.write(contents)

        return f'images/{filename.stem}{filename.suffix}'


async def bind_media_to_tweet(session: AsyncSession, ids: list, tweet_id):
    query = await session.execute(select(Media).filter(Media.id.in_(ids)))
    medias = query.scalars()
    for media in medias:
        if not media.tweet_id:
            media.tweet_id = tweet_id
    session.add_all(medias)


async def get_tweet(id: int, session: AsyncSession):
    tweet = await session.get(Tweet, id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found tweet"
        )
    return tweet


async def get_user(id: int, session: AsyncSession):
    query = await session.execute(
        select(User).where(User.id == id).options(selectinload(User.following), selectinload(User.followers))
    )
    user = query.scalars().one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found user",
        )
    return user


async def get_user_by_api_key(session: AsyncSession, key: str):
    query = await session.execute(
        select(User).where(User.api_key == key).options(selectinload(User.following), selectinload(User.followers))
    )
    return query.scalars().one_or_none()


async def get_like(session: AsyncSession, tweet_id: int, user_id: int):
    query = await session.execute(
        select(Like).where(Like.user_id == user_id, Like.tweets_id == tweet_id)
    )
    return query.scalars().one_or_none()


async def get_tweets(session: AsyncSession, user):
    query = await session.execute(
        select(Tweet).where(Tweet.user_id.in_(f.id for f in user.following)).options(selectinload(Tweet.user),
                                                                                     selectinload(Tweet.likes),
                                                                                     selectinload(Tweet.medias))
    )
    return query.scalars().all()
