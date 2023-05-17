from typing import AsyncGenerator
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from alembic.config import Config
from alembic import command

from app.main import app
from app.utils.database import get_session
from app.utils.settings import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://"
                           f"{settings.db_user}:{settings.db_password}@{settings.db_host}"
                           f":{settings.db_port}/{settings.db_test_name}")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
alembic_cfg = Config("alembic.ini")


async def override_get_db() -> AsyncGenerator:
    async with async_session() as session:
        yield session


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture
def client():
    headers = {'api-key': 'test'}
    client = AsyncClient(app=app, base_url="http://127.0.0.1:8080/api/", headers=headers)
    yield client


@pytest.fixture(autouse=True)
async def migrate():
    await migrate_db()
    yield
    await downgrage_db()
    await engine.dispose()


async def migrate_db():
    async with engine.begin() as connection:
        await connection.run_sync(__execute_upgrade)


def __execute_upgrade(connection):
    alembic_cfg.attributes["connection"] = connection
    command.upgrade(alembic_cfg, "head")


async def downgrage_db():
    async with engine.begin() as connection:
        await connection.run_sync(__execute_downgrage)


def __execute_downgrage(connection):
    alembic_cfg.attributes["connection"] = connection
    command.downgrade(alembic_cfg, "base")


@pytest.fixture
def anyio_backend():
    return "asyncio"
