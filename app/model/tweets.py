import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.database import Base


class Tweet(Base):
    __tablename__ = "tweets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now()
    )
    tweet_data: Mapped[str] = mapped_column()
    medias: Mapped[List["Media"]] = relationship(
        backref="tweet", cascade="all, delete-orphan"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    likes: Mapped[List["Like"]] = relationship(
        backref="tweet", cascade="all, delete-orphan"
    )
