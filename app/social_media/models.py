""" SocialMedia app DB models"""

from typing import Optional
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from app.user.models import UserModel

class SocialMediaModel(Base):
    """
    Represents a friend entity and defines the structure of the "character" table in the database.
    
    Fields:
    - id: An integer column representing the primary key of the "character" table.
    - first_name: A string column showing the first name of the character.
    - last_name: A string column showing the last name  of the character.
    - gender: An integer column showing the gender of the character.
    - title: A string column showing the title on the character >>> diff character diff characterStats.
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - user: The relationship column who owns this character.
    - stats: The relationship column showing the detail properties of this character.
    """
    
    __tablename__ = "social_media"
    id = Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        autoincrement=True,
    )

    youtube_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    youtube_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    youtube_is_viewed = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    youtube_view_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    facebook_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    facebook_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    facebook_followed_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)

    instagram_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    instagram_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_follow_trigger_verify_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    instagram_followed_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    instagram_tagged = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_tagged_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    instagram_reposted = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    instagram_reposted_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    telegram_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    telegram_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    telegram_followed_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    x_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    x_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    x_followed_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    discord_id = Mapped[Optional[str]] = mapped_column(String, nullable = True)
    discord_is_following = Mapped[Optional[bool]] = mapped_column(Boolean, nullable = True)
    discord_followed_date = Mapped[Optional[datetime]] = mapped_column(DateTime, nullable = True)
    
    created_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)

    user = relationship(UserModel, back_populates = "social_media")

    def __repr__(self) -> str:
        return f"<SocialMediaModel by {self.id} from user {self.user.id}>"
