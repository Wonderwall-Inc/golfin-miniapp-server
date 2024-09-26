"""Point App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core import database
from app.point import schemas
from app.point.api.v1 import service


get_db = database.get_db

router = APIRouter(prefix="/api/v1/point", tags=["point"])

@router.post("/create", response_model=schemas.PointCreateResponseSchema)
def create_point(request: schemas.PointCreateRequestSchema, db: Session = Depends(get_db)):
    """Create Point"""
    return service.create_point(request, db)


@router.get("/detail", response_model=schemas.PointRetrievalResponseSchema)
def get_point_detail(id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retrieve Point Details from Single User"""
    return service.retrieve_point(id, user_id, db)


@router.get("/details", response_model=List[schemas.PointRetrievalResponseSchema])
def get_details(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve Points by List from Multiple Users"""
    return service.retrieve_point_list(db, user_ids, skip, limit)


@router.put("/update", response_model=schemas.PointUpdateResponseSchema)
def update_point(request: schemas.PointUpdateByIdRequestSchema, db: Session = Depends(get_db)):
    """Update Point"""
    return service.update_point(request, db)

@router.get('/ranking')
def get_point_ranking(id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get Point Ranking"""
    return service.get_point_ranking(id, user_id, db)