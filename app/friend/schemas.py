from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel
# from app.user.schemas import UserSchema # Forward reference


class FriendStatusTpye(BaseModel):
    statuses: List[Literal["pending", "active", "rejected"]]


class FriendBaseSchema(BaseModel):
    """
    Base schema for Friend
    """

    id: int
    status: FriendStatusTpye
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None

    class Config:
        use_enum_values = True


class FriendUpdateDetailsSchema(BaseModel):  # what else can be updated
    """Friend Update Details Schema"""

    status: FriendStatusTpye
    custom_logs: Optional[dict] = None
    class Config:
        use_enum_values = True


class FriendSchema(BaseModel):  # all except the relationship
    """Friend Schema"""

    id: int
    status: FriendStatusTpye
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
    class Config:
        use_enum_values = True


class FriendDetailsSchema(BaseModel):  # all + relationship
    """Friend Details Schema"""

    friend_base: FriendSchema
    sender_id: int
    receiver_id: int
    # sender: UserSchema
    # receiver: UserSchema


class FriendCreateRequestSchema(BaseModel):
    """Friend Create Request Schema"""

    access_token: str
    sender_id: int
    receiver_id: int
    status: FriendStatusTpye
    class Config:
        use_enum_values = True


class FriendCreateResponseSchema(BaseModel):
    """Friend Create Response Schema"""

    friend_details: FriendDetailsSchema


class FriendRetrivalRequestSchema(BaseModel):
    """Friend Retrival Request Schema"""

    access_token: str
    id: int


class FriendRetrivalResponseSchema(BaseModel):
    """Friend Retrival Response Schema"""

    friend_details: FriendDetailsSchema


class FriendUpdateRequestSchema(BaseModel):
    """Friend Update Request Schema"""

    id: int
    access_token: str
    friend_payload: Optional[FriendUpdateDetailsSchema] = None


class FriendDetailsResponseSchema(BaseModel):
    """Friend Details Response Schema"""

    friend_details: FriendDetailsSchema
