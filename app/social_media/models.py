""" SocialMedia app DB models"""

from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class SocialMediaModel(Base):    
    __tablename__ = "social_media"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, unique=True)
    
    youtube_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    youtube_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    youtube_is_viewed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    youtube_view_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    facebook_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    facebook_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    facebook_followed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)

    instagram_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    instagram_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_follow_trigger_verify_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    instagram_followed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    instagram_tagged: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_tagged_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    instagram_reposted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_reposted_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    telegram_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    telegram_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    telegram_followed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    x_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    x_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    x_followed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    discord_id: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    discord_is_following: Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    discord_followed_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

    user = relationship("UserModel", back_populates = "social_media")

    def __repr__(self) -> str:
        return f"<SocialMediaModel by {self.id} from user {self.user.id}>"
