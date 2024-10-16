"""Point Pydantic Schemas"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class PointSchema(BaseModel):  # defaulf = false
    """Point Schema"""

    id: int
    login_amount: int  
    referral_amount: int  
    extra_profit_per_hour: int
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class PointDetailsSchema(BaseModel):
    point: PointSchema
    user_id: Optional[int] = None


class PointCreateDetailsSchema(BaseModel):
    login_amount: Optional[int] = None  
    referral_amount: Optional[int] = None  
    extra_profit_per_hour: Optional[int] = None
    custom_logs: Optional[dict] = None


class PointCreateRequestSchema(BaseModel):
    user_id: int
    access_token: str
    point_details: PointCreateDetailsSchema


class PointCreateResponseSchema(BaseModel):
    point_base: PointDetailsSchema


class PointRetrievalRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None


class PointRetrievalResponseSchema(BaseModel):
    point_base: PointDetailsSchema


class PointUpdateByIdRequestSchema(BaseModel):
    id: int
    type: str
    access_token: str
    point_payload: Optional[PointCreateDetailsSchema] = None


class PointUpdateByUserIdRequestSchema(BaseModel):
    type: str
    access_token: str
    user_id: int
    point_payload: Optional[PointCreateDetailsSchema] = None


class PointUpdateResponseSchema(BaseModel):
    point_base: PointDetailsSchema


class PointRankingList(BaseModel):
    """Point Ranking List"""

    rank: int
    total_points: int
    user_id: int
    telegram_id: str
    username: str


class PointRankingRequest(BaseModel):
    """Point Ranking Request"""
    user_id: int


class PointRankingResponse(BaseModel):
    """Point Ranking Response"""

    top_10: List[PointRankingList]
    user_info: PointRankingList
    user_in_top_10: bool
