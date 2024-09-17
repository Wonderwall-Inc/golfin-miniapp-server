from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class YoutubeSocialMediaSchema(BaseModel):
    youtube_id: Optional[str] = None
    youtube_following: Optional[bool] = None
    youtube_viewed: Optional[bool] = None
    youtube_view_date: Optional[datetime] = None


class FacebookSocialMediaSchema(BaseModel):
    facebook_id: Optional[str] = None
    facebook_following: Optional[bool] = None
    facebook_followed_date: Optional[datetime] = None


class InstagramSocialMediaSchema(BaseModel):
    instagram_id: Optional[str] = None
    instagram_following: Optional[bool] = None
    instagram_follow_trigger_verify_date: Optional[datetime] = None
    instagram_followed_date: Optional[datetime] = None
    instagram_tagged: Optional[bool] = None
    instagram_tagged_date: Optional[datetime] = None
    instagram_reposted: Optional[bool] = None
    instagram_reposted_date: Optional[datetime] = None


class TelegramSocialMediaSchema(BaseModel):
    telegram_id: Optional[str] = None
    telegram_following: Optional[bool] = None
    telegram_followed_date: Optional[datetime] = None


class XSocialMediaSchema(BaseModel):
    x_id: Optional[str] = None
    x_following: Optional[bool] = None
    x_followed_date: Optional[datetime] = None


class DiscordSocialMedia(BaseModel):
    discord_id: Optional[str] = None
    discord_following: Optional[bool] = None
    discord_followed_date: Optional[datetime] = None


class SocialMediaSchema(BaseModel):
    youtube: Optional[YoutubeSocialMediaSchema] = None
    facebook: Optional[FacebookSocialMediaSchema] = None
    instagram: Optional[InstagramSocialMediaSchema] = None
    telegram: Optional[TelegramSocialMediaSchema] = None
    x: Optional[XSocialMediaSchema] = None
    discord: Optional[DiscordSocialMedia] = None

    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class SocialMediaCategrizedBaseScehma(SocialMediaSchema):
    id: int


class SocialMediaBaseSchema(BaseModel):
    """Base schema for Social Media"""

    id: int
    youtube_id: Optional[str] = None
    youtube_following: Optional[bool] = None
    youtube_viewed: Optional[bool] = None
    youtube_view_date: Optional[datetime] = None

    facebook_id: Optional[str] = None
    facebook_following: Optional[bool] = None
    facebook_followed_date: Optional[datetime] = None

    instagram_id: Optional[str] = None
    instagram_following: Optional[bool] = None
    instagram_follow_trigger_verify_date: Optional[datetime] = None
    instagram_followed_date: Optional[datetime] = None
    instagram_tagged: Optional[bool] = None
    instagram_tagged_date: Optional[datetime] = None
    instagram_reposted: Optional[bool] = None
    instagram_reposted_date: Optional[datetime] = None

    telegram_id: Optional[str] = None
    telegram_following: Optional[bool] = None
    telegram_followed_date: Optional[datetime] = None

    x_id: Optional[str] = None
    x_following: Optional[bool] = None
    x_followed_date: Optional[datetime] = None

    discord_id: Optional[str] = None
    discord_following: Optional[bool] = None
    discord_followed_date: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class SocialMediaCreateDetailScheam(BaseModel):  # without id
    youtube: Optional[YoutubeSocialMediaSchema] = None
    facebook: Optional[FacebookSocialMediaSchema] = None
    instagram: Optional[InstagramSocialMediaSchema] = None
    telegram: Optional[TelegramSocialMediaSchema] = None
    x: Optional[XSocialMediaSchema] = None
    discord: Optional[DiscordSocialMedia] = None
    custom_logs: Optional[dict] = None


class SocialMediaCreateRequestSchema(BaseModel):
    user_id: int
    access_token: str
    type: str  # FIXME: enum
    social_media: SocialMediaCreateDetailScheam


class SocialMediaCreateResponseSchema(BaseModel):
    user_id: int
    social_media: SocialMediaBaseSchema


class SocialMediaDetailsSchema(BaseModel):
    social_media: SocialMediaBaseSchema


class SocialMediaRetrievalRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None


class SocialMediaRetrievalResponseSchema(BaseModel):
    user_id: int
    social_media: SocialMediaBaseSchema


class SocialMediaUpdateRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None
    type: str  # FIXME: enum
    social_media: SocialMediaCreateDetailScheam


class SocialMediaUpdateResponseSchema(BaseModel):
    user_id: int
    social_media: SocialMediaCategrizedBaseScehma

# TikTokSocialMediaSchema,
# PinterestSocialMediaSchema,
# RedditSocialMediaSchema,
# DiscordSocialMediaSchema,
# TwitchSocialMediaSchema,
# PatreonSocialMediaSchema,

