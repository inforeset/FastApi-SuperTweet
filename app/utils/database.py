from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.utils.settings import get_settings

settings = get_settings()

DATABASE_URL = (f"postgresql+asyncpg://"
                f"{settings.db_user}:{settings.db_password}@{settings.db_host}"
                f":{settings.db_port}/{settings.db_name}")

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
