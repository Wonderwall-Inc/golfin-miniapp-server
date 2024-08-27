"""
Character App Pydantic Schemas (Based on Reference)
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CharacterStatsSchema(BaseModel):
    """Character Stats Schema (Matches Reference)"""

    level: int
    exp_points: int
    # Adjusted field names based on model (strength -> stamina, etc.)
    stamina: int  # (strength from reference)
    recovery: int  # (driving from reference)
    condition: int  # (club_control from reference)
    # Removed spin and putt fields not present in the model


class CharacterDetailsSchema(BaseModel):
    """Character Details Schema (Matches Reference with Model Adjustments)"""

    character_id: Optional[int]
    first_name: str
    last_name: str
    gender: int


class CharacterDetailsRequestSchema(BaseModel):
    """Character Details Request Schema (Matches Reference)"""

    first_name: str
    last_name: str
    gender: int


class CharacterCreateRequestSchema(BaseModel):
    """Character Create Request Schema (Matches Reference)"""

    user_id: int
    access_token: str
    character_details: CharacterDetailsRequestSchema


class CharacterCreateResponseSchema(BaseModel):
    """Character Create Response Schema (Matches Reference)"""

    character_id: int
    character_stats: CharacterStatsSchema


class CharacterDetailResponseSchema(BaseModel):
    """Character Detail Response Schema (Matches Reference)"""

    character_details: CharacterDetailsSchema


class CharacterStatsResponseSchema(BaseModel):
    """Character Stats Response Schema (Matches Reference)"""

    character_stats: CharacterStatsSchema


class CharacterUpdateRequestSchema(BaseModel):
    """Character Update Request Schema (Matches Reference)"""

    user_id: int
    access_token: str
    character_id: int
    character_details: Optional[CharacterDetailsRequestSchema] = None
    character_stats: Optional[CharacterStatsSchema] = None


class CharacterUpdateResponseSchema(BaseModel):
    """Character Update Response Schema (Matches Reference)"""

    character_details: CharacterDetailsSchema
    character_stats: CharacterStatsSchema


class GameCharacterBaseSchema(BaseModel):
    """
    Base schema for Game Character
    """
    id: int
    first_name: str
    last_name: str
    gender: int  # Assuming gender is an integer
    title: str
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
