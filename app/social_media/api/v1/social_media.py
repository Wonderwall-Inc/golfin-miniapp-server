"""User App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from core import database

from app.social_media import schemas
from app.social_media.api.v1 import service
from app.social_media import schemas


router = APIRouter(prefix="/api/v1/social_media", tags=["social_media"])
get_db = database.get_db


@router.post("/create", response_model=schemas.SocialMediaCreateResponseSchema)
def create_social_media(
    request: schemas.SocialMediaCreateRequestSchema, db: Session = Depends(get_db)
):
    """Create a new social media"""
    return service.create_social_media(request, db)


@router.get("/detail", response_model=schemas.SocialMediaRetrievalResponseSchema)
def get_social_media(
    id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return service.retrieve_social_media(id, user_id, db)


@router.get("/details", response_model=List[schemas.SocialMediaRetrievalResponseSchema])
def get_details(user_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    return service.retrieve_social_media_list(user_ids, db)


@router.put("/update", response_model=schemas.SocialMediaUpdateResponseSchema)
def update_social_media(
    request: schemas.SocialMediaUpdateRequestSchema, db: Session = Depends(get_db)
):
    return service.update_social_media(request, db)
