"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.social_media import schemas
from app.social_media.api.v1 import service


router = APIRouter(prefix="/api/v1/social_media", tags=["social_media"])

@router.get('/')
def hello():
    return "social_media"
