"""Users Pydantic Schemas"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.game_character.schemas import GameCharacterBaseSchema
from app.point.schemas import PointScehma
from app.activity.schemas import ActivityBaseSchema
from app.social_media.schemas import SocialMediaBaseSchema
from app.friend.schemas import FriendBaseSchema, FriendIds


class UserBaseSchema(BaseModel):  # default = False
    """User Base Schema"""

    username: str
    telegram_id: str
    token_balance: int
    is_active: bool
    is_premium: bool


class UserPersonalInfoSchema(BaseModel):
    """User personal Info Schema"""

    location: str
    nationality: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None


class UserTelegramInfoSchema(BaseModel):
    username: str
    telegram_id: str
    token_balance: int
    is_premium: bool
    wallet_address: Optional[str] = None
    chat_id: str


class UserAppInfoSchema(BaseModel):
    is_active: bool
    in_game_items: Optional[dict] = None
    is_admin: Optional[bool] = None
    skin: List[str]
    custom_logs: Optional[dict] = None


class UserUpdateDetailsSchema(BaseModel):
    """User Update Detail Schema"""

    token_balance: int
    is_active: bool
    is_premium: bool
    in_game_items: Optional[dict] = None
    skin: List[str]
    location: str
    age: int
    custom_logs: Optional[dict] = None


class UserSchema(BaseModel):
    id: int
    app_info: UserAppInfoSchema
    personal_info: UserPersonalInfoSchema
    telegram_info: UserTelegramInfoSchema
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class UserDetailsSchema(BaseModel):  # show the based + relationship
    """User Display Schema"""

    user_base: UserSchema
    game_characters: Optional[List[GameCharacterBaseSchema]] = []
    point: Optional[List[PointScehma]] = []
    activity: Optional[List[ActivityBaseSchema]] = []
    social_media: Optional[List[SocialMediaBaseSchema]] = []
    sender: Optional[List[FriendBaseSchema]] = []  # friends are multiple as list
    receiver: Optional[List[FriendBaseSchema]] = []  # friends are multiple as list

    class Config:
        """Pydantic Model Config"""

        from_attributes = True


class UserCreateRequestSchema(BaseModel):
    """User Create Request Schema"""

    access_token: Optional[str] = None
    app_info: UserAppInfoSchema
    personal_info: UserPersonalInfoSchema
    telegram_info: UserTelegramInfoSchema


class UserCreateResponseSchema(BaseModel):
    """User Create Response Schema"""

    access_token: Optional[str] = None
    user_details: UserDetailsSchema


class UserRetrivalRequestSchema(BaseModel):
    """User Access Request Schema"""

    # Define fields for access request data as needed
    access_token: str
    id: Optional[str] = None
    username: Optional[str] = None
    telegram_id: Optional[str] = None
    wallet_address: Optional[str] = None
    personal_info: UserPersonalInfoSchema


class UserRetrivalResponseSchema(BaseModel):
    """User Access Response Schema"""

    user_details: UserDetailsSchema


class UserUpdateRequestSchema(BaseModel):
    """User Update Request Schema"""

    id: int
    access_token: str
    user_payload: Optional[UserUpdateDetailsSchema] = None


class UserUpdateResponseSchema(BaseModel):
    """User Update Response Schema"""

    user_details: UserDetailsSchema


class UserDetailsResponseSchema(BaseModel):
    """User Details Response Schema"""

    user_details: UserDetailsSchema
