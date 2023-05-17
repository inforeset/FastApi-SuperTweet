from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.utils.database import Base


class Like(Base):
    __tablename__ = "likes"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    tweets_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"))
