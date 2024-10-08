from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.point.schemas import PointSchema

class ActivityBaseSchema(BaseModel):
    """
    Base schema for Activity
    """

    id: int
    logged_in: bool
    login_streak: int
    total_logins: int
    last_action_time: Optional[datetime] = None
    last_login_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class ActivitySchema(BaseModel):
    logged_in: bool
    login_streak: int
    total_logins: int
    last_action_time: Optional[datetime] = None
    last_login_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class ActivityCreateDetailSchema(BaseModel):
    custom_logs: Optional[dict] = None


class ActivityUpdateDetailSchema(ActivityCreateDetailSchema):
    logged_in: Optional[bool] = None
    login_streak: Optional[int] = None
    total_logins: Optional[int] = None
    last_action_time: Optional[datetime] = None
    last_login_time: Optional[datetime] = None


class ActivityCreateRequestSchema(BaseModel):
    user_id: int
    access_token: str
    activity: ActivityCreateDetailSchema


class ActivityCreateResponseSchema(BaseModel):
    user_id: int
    activity: ActivityBaseSchema


class ActivityDetailSchema(BaseModel):
    activity: ActivityBaseSchema


class ActivityRetrievalRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None


class ActivityRetrievalResponseSchema(BaseModel):
    user_id: int
    activity: ActivityBaseSchema


class ActivityUpdateRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None
    activity: ActivityUpdateDetailSchema


class ActivityUpdateResponseSchema(BaseModel):
    user_id: int
    activity: ActivityBaseSchema


class DailyCheckInRequestSchema(BaseModel):
    user_id: int
    access_token: str

class DailyCheckInResponseSchema(BaseModel):
    activity: ActivityBaseSchema
    point: PointSchema