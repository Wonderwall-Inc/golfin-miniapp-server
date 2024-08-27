"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.user import schemas
from app.user.api.v1 import service


router = APIRouter(prefix="/api/v1/friend", tags=["friend"])

@router.get('/')
def hello():
    return "friend"