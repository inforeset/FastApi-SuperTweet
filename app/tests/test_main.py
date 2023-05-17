import os
import shutil
import uuid

import pytest
from _pytest._py.path import LocalPath
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.tests.conftest import engine
from app.utils.settings import MEDIA_ROOT


@pytest.mark.anyio
async def test_get_me(client: AsyncClient):
    await_response = {
        "result": True,
        "user": {
            "id": 1,
            "username": "test1",
            "following": [
                {
                    "id": 2,
                    "username": "test2"
                }
            ],
            "followers": [
                {
                    "id": 2,
                    "username": "test2"
                }
            ]
        }
    }
    response = await client.get("users/me")
    assert response.status_code == 200
    assert response.json() == await_response


@pytest.mark.anyio
async def test_get_user(client: AsyncClient):
    await_response = {
        "result": True,
        "user": {
            "id": 2,
            "username": "test2",
            "following": [
                {
                    "id": 1,
                    "username": "test1"
                }
            ],
            "followers": [
                {
                    "id": 1,
                    "username": "test1"
                }
            ]
        }
    }
    response = await client.get("users/2")
    assert response.status_code == 200
    assert response.json() == await_response


@pytest.mark.anyio
async def test_get_user_with_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found user"
    }
    response = await client.get("users/50")
    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_follow(client: AsyncClient):
    await_response = {
        "result": True
    }
    response = await client.post("users/3/follow")
    assert response.status_code == 200
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        following = await session.execute(
            text(
                "SELECT * "
                "FROM user_to_user "
                "WHERE user_to_user.followers_id = 1 AND user_to_user.following_id = 3"
            )
        )
    results_as_dict = following.mappings().all()
    assert len(results_as_dict) == 1


@pytest.mark.anyio
async def test_follow_with_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found user"
    }
    response = await client.post("users/50/follow")
    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_delete_follow(client: AsyncClient):
    await_response = {
        "result": True
    }
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO user_to_user(followers_id, following_id)"
                "VALUES(1, 3);"
            )
        )
        await session.commit()
    response = await client.delete("users/3/follow")
    assert response.status_code == 200
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        following = await session.execute(
            text(
                "SELECT * "
                "FROM user_to_user "
                "WHERE user_to_user.followers_id = 1 AND user_to_user.following_id = 3;"
            )
        )
    results_as_dict = following.mappings().all()
    assert len(results_as_dict) == 0


@pytest.mark.anyio
async def test_delete_follow_with_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found user"
    }
    response = await client.delete("users/50/follow")
    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_get_tweets(client: AsyncClient):
    await_response = {
        "result": True,
        "tweets": [
            {
                "id": 1,
                "content": "test_tweet2",
                "author": {
                    "id": 2,
                    "username": "test2"
                },
                "likes": [],
                "attachments": [
                    "test.jpg"
                ]
            }
        ]
    }
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tweets(created_at, tweet_data, user_id)"
                "VALUES('2023-04-13 20:35:10.817870', 'test_tweet2', 2);"
            )
        )
        await session.execute(
            text(
                "INSERT INTO medias(path_media, tweet_id)"
                "VALUES('test.jpg', 1);"
            )
        )
        await session.commit()

    response = await client.get("tweets")
    assert response.status_code == 200
    assert response.json() == await_response


@pytest.mark.anyio
async def test_create_tweet(client: AsyncClient):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO medias(path_media, tweet_id)"
                "VALUES('test.jpg', NULL);"
            )
        )
        await session.commit()

    data = {
        "tweet_data": "test_tweet",
        "tweet_media_ids": [1]
    }

    await_response = {
        "result": True,
        "tweet_id": 1
    }
    response = await client.post("tweets", json=data)
    assert response.status_code == 201
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        tweet = await session.execute(
            text(
                "SELECT * "
                "FROM tweets "
                "WHERE tweets.id = 1;"
            )
        )
    results_as_dict = tweet.mappings().all()
    assert len(results_as_dict) == 1
    assert results_as_dict[0]['tweet_data'] == "test_tweet"


@pytest.mark.anyio
async def test_delete_tweet(client: AsyncClient):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tweets(created_at, tweet_data, user_id)"
                "VALUES('2023-04-13 20:36:10.817870', 'test_tweet', 1);"
            )
        )
        await session.commit()

    await_response = {
        "result": True
    }

    response = await client.delete("tweets/1")

    assert response.status_code == 200
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        tweet = await session.execute(
            text(
                "SELECT * "
                "FROM tweets "
                "WHERE tweets.id = 1;"
            )
        )
    results_as_dict = tweet.mappings().all()
    assert len(results_as_dict) == 0


@pytest.mark.anyio
async def test_delete_tweet_not_owner(client: AsyncClient):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tweets(created_at, tweet_data, user_id)"
                "VALUES('2023-04-13 20:36:10.817870', 'test_tweet', 2);"
            )
        )
        await session.commit()

    await_response = {
        "result": False,
        "error_type": "Forbidden",
        "error_message": "Access forbidden"
    }

    response = await client.delete("tweets/1")

    assert response.status_code == 403
    assert response.json() == await_response


@pytest.mark.anyio
async def test_delete_tweet_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found tweet"
    }

    response = await client.delete("tweets/50")

    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_likes(client: AsyncClient):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tweets(created_at, tweet_data, user_id)"
                "VALUES('2023-04-13 20:36:10.817870', 'test_tweet', 2);"
            )
        )
        await session.commit()

    await_response = {
        "result": True
    }

    response = await client.post("tweets/1/likes")

    assert response.status_code == 200
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        like = await session.execute(
            text(
                "SELECT * "
                "FROM likes "
                "WHERE likes.id = 1;"
            )
        )
    results_as_dict = like.mappings().all()
    assert len(results_as_dict) == 1


@pytest.mark.anyio
async def test_likes_with_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found tweet"
    }

    response = await client.post("tweets/50/likes")

    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_delete_like(client: AsyncClient):
    async with AsyncSession(engine) as session:
        await session.execute(
            text(
                "INSERT INTO tweets(created_at, tweet_data, user_id)"
                "VALUES('2023-04-13 20:36:10.817870', 'test_tweet', 2);"
            )
        )
        await session.execute(
            text(
                "INSERT INTO likes(user_id, tweets_id)"
                "VALUES(1, 1);"
            )
        )
        await session.commit()

    await_response = {
        "result": True
    }

    response = await client.delete("tweets/1/likes")

    assert response.status_code == 200
    assert response.json() == await_response
    async with AsyncSession(engine) as session:
        like = await session.execute(
            text(
                "SELECT * "
                "FROM likes "
                "WHERE likes.id = 1;"
            )
        )
    results_as_dict = like.mappings().all()
    assert len(results_as_dict) == 0


@pytest.mark.anyio
async def test_delete_like_with_bad_id(client: AsyncClient):
    await_response = {
        "result": False,
        "error_type": "Not Found",
        "error_message": "Not Found tweet"
    }

    response = await client.delete("tweets/50/likes")

    assert response.status_code == 404
    assert response.json() == await_response


@pytest.mark.anyio
async def test_media(tmpdir: LocalPath, client: AsyncClient):
    await_response = {
        "result": True,
        "media_id": 1
    }
    name = f"test_{uuid.uuid4()}.jpg"
    img = tmpdir.join(name)
    img.write('test')
    response = await client.post("medias", files={"file": open(img, "rb")})

    assert response.status_code == 201
    assert response.json() == await_response
    path = os.path.join(MEDIA_ROOT, name)
    if os.path.isfile(path):
        os.remove(path)
