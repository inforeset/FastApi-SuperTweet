from typing import List, Optional

from sqlalchemy import ForeignKey, Table, Column, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref

from app.utils.database import Base

user_to_user = Table(
    "user_to_user",
    Base.metadata,
    Column("followers_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    tweets: Mapped[List["Tweet"]] = relationship(backref="user", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(backref="user", cascade="all, delete-orphan")
    api_key: Mapped[str] = mapped_column()
    following = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.followers_id,
        secondaryjoin=id == user_to_user.c.following_id,
        backref="followers",
        lazy="selectin"
    )
