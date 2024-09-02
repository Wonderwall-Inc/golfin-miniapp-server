from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel

FriendStatusTpye = Literal["pending", "active", "rejected"]


class FriendIds(BaseModel):
    sender_id: int
    id: int
    receiver_id: int


class FriendBaseSchema(BaseModel):
    """Base schema for Friend"""

    sender_id: int
    status: FriendStatusTpye
    id: int
    updated_at: datetime
    receiver_id: int
    created_at: datetime
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


class FriendWithIdsRetrivalResponseSchema(BaseModel):
    sender: Optional[List[FriendBaseSchema]] = None
    receiver: Optional[List[FriendBaseSchema]] = None


class FriendRetrivalResponseSchema(BaseModel):
    """Friend Retrival Response Schema"""

    friend_details: FriendDetailsSchema


class FriendUpdateByIdRequestSchema(BaseModel):
    """Update the friend by status and user id"""

    id: Optional[int] = None
    access_token: str
    friend_payload: FriendUpdateDetailsSchema


class FriendUpdateBySenderIdRequestSchema(BaseModel):
    """Update the friend by status and sender id"""

    sender_id: Optional[int] = None
    access_token: str
    friend_payload: FriendUpdateDetailsSchema


class FriendUpdateByReceiverIdRequestSchema(BaseModel):
    receiver_id: Optional[int] = None
    access_token: str
    friend_payload: FriendUpdateDetailsSchema


class FriendDetailsResponseSchema(BaseModel):
    """Friend Details Response Schema"""

    friend_details: FriendDetailsSchema
