"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from core import database

from app.point import schemas
from app.point.api.v1 import service


router = APIRouter(prefix="/api/v1/point", tags=["point"])
get_db = database.get_db


@router.post("/create", response_model=schemas.PointCreateResponseSchema)
def create_point(
    request: schemas.PointCreateRequestSchema, db: Session = Depends(get_db)
):
    """Create point"""
    return service.create_point(request, db)


@router.get("/detail/id/{id}", response_model=schemas.PointRetrivalResponseSchema)
def get_detail_by_point_id(id: int, db: Session = Depends(get_db)):
    """Get the point detail based on point id"""
    return service.retrieve_point_by_point_id(id, db)


@router.get("/detail/{user_id}", response_model=schemas.PointRetrivalResponseSchema)
def get_detail_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """Get the point detail based on user id"""
    return service.retrieve_point_by_user_id(user_id, db)


@router.get("/details", response_model=List[int])
def get_details(user_ids: List[int] = Query(...), db: Session = Depends(get_db)):
    """Get the points by list of integers"""
    return service.retrieve_points(user_ids, db)


@router.put("/update/id")
def update_point(
    request: schemas.PointUpdateByIdRequestSchema, db: Session = Depends(get_db)
):
    """Update the point"""
    return service.update_point_by_id(request, db)
