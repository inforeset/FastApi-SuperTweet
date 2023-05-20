from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.utils.database import get_session
from app.utils.utils import get_user_by_api_key

api_key_header = APIKeyHeader(name="api-key")


async def get_current_user(
    api_key_header: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
):
    """Возвращает пользователя из базы данных по API ключу."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"api-key": ""},
    )
    user = await get_user_by_api_key(session, key=api_key_header)
    if user is None:
        raise credentials_exception
    return user
