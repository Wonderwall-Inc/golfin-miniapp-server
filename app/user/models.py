"""User app DB models"""

from datetime import datetime
from typing import Optional, Set, Literal, get_args, List
from sqlalchemy.orm import relationship, mapped_column, Mapped, backref
from sqlalchemy import Integer, String, Boolean, JSON, DateTime, Enum, ForeignKey

from core.database import Base
from app.game_character.models import GameCharacterModel
from app.activity.models import ActivityModel
from app.social_media.models import SocialMediaModel
from app.friend.models import FriendModel
from app.point.models import PointModel


class UserModel(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telegram_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    token_balance: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)

    wallet_address: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )  # REVIEW: allow mutliple?
    in_game_items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    access_token: Mapped[Optional[str]] = mapped_column(String(2000), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    skin: Mapped[List[str]] = mapped_column(JSON, default=lambda: ["Default"])

    chat_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    start_param: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    location: Mapped[str] = mapped_column(String(100), nullable=False)
    nationality: Mapped[str] = mapped_column(String(100), nullable=False)

    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

    game_characters: Mapped[Set["GameCharacterModel"]] = relationship(
        back_populates="user"
    )
    point = relationship(PointModel, back_populates="user")
    activity = relationship(ActivityModel, back_populates="user")
    social_media = relationship(SocialMediaModel, back_populates="user")
    sender = relationship(
        "FriendModel", foreign_keys="FriendModel.sender_id", back_populates="sender"
    )
    receiver = relationship(
        "FriendModel", foreign_keys="FriendModel.receiver_id", back_populates="receiver"
    )

    def __repr__(self) -> str:
        return f"<UserModel telegram id={self.telegram_id} username={self.username}>"
