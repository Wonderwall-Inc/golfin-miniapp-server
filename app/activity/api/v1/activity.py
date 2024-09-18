"""Activity App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core import database
from app.activity import schemas
from app.activity.api.v1 import service


get_db = database.get_db

router = APIRouter(prefix="/api/v1/activity", tags=["activity"])

@router.post('/create', response_model=schemas.ActivityCreateResponseSchema)
def create_activity(request: schemas.ActivityCreateRequestSchema, db: Session=Depends(get_db)):
    """Create Activity"""
    return service.create_activity(request, db)

@router.get('/detail', response_model=schemas.ActivityRetrievalResponseSchema)
def get_activity(id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retrieve Activity Details from Single User"""
    return service.retrieve_activity(id, user_id, db) 

@router.get('/details', response_model=List[schemas.ActivityRetrievalResponseSchema])
def get_activity_details(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session=Depends(get_db)):
    """Retrieve Activities by List from Multiple Users"""
    return service.retrieve_activity_list(db, user_ids, skip, limit) 

@router.put('/update', response_model=schemas.ActivityUpdateResponseSchema)
def update_activity(request: schemas.ActivityUpdateRequestSchema, db: Session=Depends(get_db)):
    """Update Activity"""
    return service.update_activity(request, db) 

@router.put('/update/logged-in')
def update_activity(db: Session=Depends(get_db)):
    """Update Activity"""
    return service.update_activity_logged_in(db) 
