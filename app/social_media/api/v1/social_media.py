"""Social Media App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core import database
from app.social_media import schemas
from app.social_media.api.v1 import service


get_db = database.get_db

router = APIRouter(prefix="/api/v1/social_media", tags=["social_media"])


@router.post("/create", response_model=schemas.SocialMediaCreateResponseSchema)
def create_social_media(request: schemas.SocialMediaCreateRequestSchema, db: Session = Depends(get_db)):
    """Create Social Media"""
    return service.create_social_media(request, db)


@router.get("/detail", response_model=schemas.SocialMediaRetrievalResponseSchema)
def get_social_media(id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retrieve Social Media Details from Single User"""
    return service.retrieve_social_media(id, user_id, db)


@router.get("/details", response_model=List[schemas.SocialMediaRetrievalResponseSchema])
def get_details(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve Social Media by List from Multiple Users"""
    return service.retrieve_social_media_list(db, user_ids, skip, limit)


@router.put("/update", response_model=schemas.SocialMediaUpdateResponseSchema)
def update_social_media(request: schemas.SocialMediaUpdateRequestSchema, db: Session = Depends(get_db)):
    """Update Social Media"""
    return service.update_social_media(request, db)
