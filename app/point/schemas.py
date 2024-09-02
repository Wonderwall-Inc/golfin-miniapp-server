"""Point Pydantic Schemas"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PointScehma(BaseModel):  # defaulf = false
    """Point Schema"""

    id: int
    amount: int  # Assuming gender is an integer
    extra_profit_per_hour: int
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class PointDetailsSchema(BaseModel):
    point: PointScehma
    user_id: Optional[int] = None


class PointCreateDetailsSchema(BaseModel):
    amount: int
    extra_profit_per_hour: int
    custom_logs: Optional[dict] = None


class PointCreateRequestSchema(BaseModel):
    user_id: int
    access_token: str
    point_details: PointCreateDetailsSchema


class PointCreateResponseSchema(BaseModel):
    point_base: PointDetailsSchema


class PointRetrivalRequestSchema(BaseModel):
    access_token: str
    id: int
    user_id: Optional[int] = None


class PointRetrivalResponseSchema(BaseModel):
    point_base: PointDetailsSchema


class PointUpdateByIdRequestSchema(BaseModel):
    type: str
    access_token: str
    id: int
    point_payload: Optional[PointCreateDetailsSchema] = None


class PointUpdateByUserIdRequestSchema(BaseModel):
    type: str
    access_token: str
    user_id: int
    point_payload: Optional[PointCreateDetailsSchema] = None


class PointUpdateResponseSchema(BaseModel):
    point_base: PointDetailsSchema
