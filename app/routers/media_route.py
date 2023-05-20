from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.media import Media
from app.schemas.media_schema import MediaOut
from app.schemas.user_schema import User
from app.utils.authentication import get_current_user
from app.utils.database import get_session
from app.utils.utils import write_file

router = APIRouter()


@router.post("/medias", response_model=MediaOut, status_code=201)
async def create_upload_file(
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile | None = None,
    session: AsyncSession = Depends(get_session),
):
    """Загрузка файла"""
    if not file:
        return {"message": "No upload file sent"}
    new_filename = await write_file(file)
    if new_filename:
        new_file = Media(path_media=new_filename)
        session.add(new_file)
        await session.commit()
        return new_file
