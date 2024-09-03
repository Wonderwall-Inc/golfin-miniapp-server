"""User App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from core import database

from app.activity import schemas
from app.activity.api.v1 import service


router = APIRouter(prefix="/api/v1/activity", tags=["activity"])
get_db = database.get_db

@router.post('/create', response_model=schemas.ActivityCreateResponseSchema)
def create_activity(request: schemas.ActivityCreateRequestSchema, db: Session=Depends(get_db)):
    return service.create_activity(request, db)

@router.get('/detail', response_model=schemas.ActivityRetrievalResponseSchema)
def get_activity(
    id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return service.retrieve_activity(id, user_id, db) 

@router.get('/details', response_model=List[schemas.ActivityRetrievalResponseSchema])
def get_activity_details(request: List[int]=Query(...), db: Session=Depends(get_db)): 
    return
    return service.get_activity_details(request, db) 

@router.put('/update', response_model=schemas.ActivityUpdateResponseSchema)
def update_activity(request: schemas.ActivityUpdateRequestSchema, db: Session=Depends(get_db)):
    return
    return service.update_activity(request, db) 
