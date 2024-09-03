"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.activity import schemas
from app.activity.api.v1 import service


router = APIRouter(prefix="/api/v1/activity", tags=["activity"])
get_db = database.get_db()

