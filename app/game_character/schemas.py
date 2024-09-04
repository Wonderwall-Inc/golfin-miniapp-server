"""
Character App Pydantic Schemas (Based on Reference)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class GameCharacterBaseSchema(BaseModel):
    """Game Character Schema"""

    id: int
    first_name: str
    last_name: str
    gender: int  # Assuming gender is an integer
    title: str
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class GameCharacterStatBaseSchema(BaseModel):
    """Game Character Stat Schema"""

    id: int
    level: int
    exp_points: int
    stamina: int
    recovery: int
    condition: int


class GameCharacterStatsSchema(BaseModel):
    """Game Character Stats Schema (Matches Reference)"""

    id: int
    level: int
    exp_points: int
    # Adjusted field names based on model (strength -> stamina, etc.)
    stamina: int  # (strength from reference)
    recovery: int  # (driving from reference)
    condition: int  # (club_control from reference)
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None

    # Removed spin and putt fields not present in the model


class GameCharacterSchema(BaseModel):
    """Game Character Schema"""

    id: int
    first_name: str
    last_name: str
    gender: int
    title: str
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None


class GameCharacterDetailsSchema(BaseModel):  # Base + relationship
    """Game Character Details Schema (Matches Reference with Model Adjustments)"""

    game_character_base: GameCharacterSchema
    # user_id: int


class GameCharacterStatDetailsSchema(BaseModel):
    """Game Character Stat Details Schema"""

    game_character_stat_base: GameCharacterStatsSchema
    game_character_id: Optional[int] = None


class GameCharacterCreateDetailsSchema(BaseModel):
    """Game Character Create Details Schema"""

    first_name: str
    last_name: str
    gender: int
    title: str
    custom_logs: Optional[dict] = None


class GameCharacterUpdateDetailsSchema(
    BaseModel
):  # except the id, what else need to be used during update
    """Game Character Update Details Schema"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[int] = None
    title: Optional[str] = None
    custom_logs: Optional[dict] = None


class GameCharacterStatsUpdateDetailsSchema(
    BaseModel
):  # except the id, what need to be used for update?
    """Game Character Stat Update Details Schema"""

    level: Optional[int] = None
    exp_points: Optional[int] = None
    stamina: Optional[int] = None
    recovery: Optional[int] = None
    condition: Optional[int] = None
    custom_logs: Optional[dict] = None


class GameCharacterCreateRequestSchema(BaseModel):  # fKey, access token, payload
    """Game Character Create Request Schema (Matches Reference)"""

    user_id: int
    access_token: str
    character_details: GameCharacterCreateDetailsSchema


class GameCharacterCreateResponseSchema(BaseModel):
    """Game Character Create Response Schema (Matches Reference)"""

    game_character_id: int
    character_stats: GameCharacterStatsSchema


class GameCharacterRetrievalRequestSchema(BaseModel):
    """Game Character Retrieval Request Schema"""

    access_token: str
    id: int
    character_details: Optional[GameCharacterDetailsSchema] = None


class GameCharacterRetrievalResponseSchema(BaseModel):
    """Game Character Retrieval Response Schema"""

    character_details: GameCharacterDetailsSchema
    character_stats: List[GameCharacterStatDetailsSchema]


class GameCharacterStatRetrievalRequestSchema(BaseModel):
    """Game Character Stats Retrieval Request Schema"""

    access_token: str
    id: int
    character_stats: Optional[GameCharacterStatDetailsSchema] = None


class GameCharacterStatRetrievalResponseSchema(BaseModel):
    """Game Character Stats Retrieval Response Schema"""

    game_character_id: int
    character_stats: GameCharacterStatsSchema


# FIXME:
class GameCharacterUpdateRequestSchema(BaseModel):
    """Game Character Update Request Schema (Matches Reference)"""

    user_id: int
    access_token: str
    game_character_id: int
    character_details: Optional[GameCharacterUpdateDetailsSchema] = None
    character_stats: Optional[GameCharacterStatsUpdateDetailsSchema] = None


class GameCharacterUpdateResponseSchema(BaseModel):
    """Character Update Response Schema (Matches Reference)"""

    character_details: GameCharacterSchema
    character_stats: GameCharacterStatsSchema
