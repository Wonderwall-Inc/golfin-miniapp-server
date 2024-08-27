"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.game_character import schemas
from app.game_character.api.v1 import service


router = APIRouter(prefix="/api/v1/game_character", tags=["game_character"])

@router.get('/')
def hello():
    return "game_character"
