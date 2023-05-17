from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.schemas.base_schema import BaseSchema
from app.schemas.user_schema import Token, User, UserOut
from app.utils.authentication import get_current_user
from app.utils.database import get_session
from app.utils.settings import RESPONSE_401_422_404_400, RESPONSE_401_422_404, RESPONSE_401
from app.utils.utils import get_user

router = APIRouter()


@router.post("/users/{id}/follow", response_model=BaseSchema, responses=RESPONSE_401_422_404_400, status_code=200)
async def follow(
        id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_session)
):
    user = await get_user(id, session)
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can't follow yourself",
        )
    if user not in current_user.following:
        cur_user_db = await get_user(current_user.id, session)
        cur_user_db.following.append(user)
        await session.commit()
    return "Ok"


@router.delete("/users/{id}/follow", response_model=BaseSchema, responses=RESPONSE_401_422_404, status_code=200)
async def delete_follow(
        id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_session)
):
    user = await get_user(id, session)
    if user in current_user.following:
        cur_user_db = await get_user(current_user.id, session)
        cur_user_db.following.remove(user)
        await session.commit()
    return "Ok"


@router.get("/users/me", response_model=UserOut, responses=RESPONSE_401, status_code=200)
async def get_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return {'user': current_user}


@router.get("/users/{id}", response_model=UserOut, responses=RESPONSE_401_422_404, status_code=200)
async def get_users(
        id: int,
        current_user: Annotated[User, Depends(get_current_user)],
        session: AsyncSession = Depends(get_session)
):
    user = await get_user(id, session)
    return {'user': user}
