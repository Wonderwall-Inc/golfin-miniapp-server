"""Record App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core import database
from app.record import schemas
from app.record.api.v1 import service


get_db = database.get_db

router = APIRouter(prefix="/api/v1/record", tags=["record"])

@router.post("/create", response_model=schemas.RecordCreateResponseSchema)
def create_record(request: schemas.RecordCreateRequestSchema, db: Session = Depends(get_db)):
    """Create Record"""
    return service.create_record(request, db)


@router.get("/detail", response_model=schemas.RecordRetrievalResponseSchema)
def get_record_detail(id: Optional[int] = None, user_id: Optional[int] = None,db: Session = Depends(get_db)):
    """Retrieve Record Details from Single User"""
    return service.retrieve_record(id, user_id, db)


@router.get("/details", response_model=List[schemas.RecordRetrievalResponseSchema])
def get_details(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve Records by List from Multiple Users"""
    return service.retrieve_record_list(db, user_ids, skip, limit)


#@router.put("/update", response_model=schemas.RecordUpdateResponseSchema)
#def update_record(request: schemas.RecordUpdateByIdRequestSchema, db: Session = Depends(get_db)):
#    """Update Record"""
#    return service.update_record(request, db)