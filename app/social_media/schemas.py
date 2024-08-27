from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SocialMediaBaseSchema(BaseModel):
    """
    Base schema for Social Media
    """

    id: int
    youtube_id: Optional[str]
    youtube_is_following: Optional[bool]
    youtube_is_viewed: Optional[bool]
    youtube_view_date: Optional[datetime]

    facebook_id: Optional[str]
    facebook_is_following: Optional[bool]
    facebook_followed_date: Optional[datetime]

    instagram_id: Optional[str]
    instagram_is_following: Optional[bool]
    instagram_follow_trigger_verify_date: Optional[datetime]
    instagram_followed_date: Optional[datetime]
    instagram_tagged: Optional[bool]
    instagram_tagged_date: Optional[datetime]
    instagram_reposted: Optional[bool]
    instagram_reposted_date: Optional[datetime]

    telegram_id: Optional[str]
    telegram_is_following: Optional[bool]
    telegram_followed_date: Optional[datetime]

    x_id: Optional[str]
    x_is_following: Optional[bool]
    x_followed_date: Optional[datetime]

    discord_id: Optional[str]
    discord_is_following: Optional[bool]
    discord_followed_date: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
