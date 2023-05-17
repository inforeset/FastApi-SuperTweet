from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.database import Base


class Media(Base):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    path_media: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=True)