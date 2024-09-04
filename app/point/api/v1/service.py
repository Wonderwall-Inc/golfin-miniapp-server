"""Point App Business Logics"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.point import schemas
from app.point.models import PointModel

def create_point(request: schemas.PointCreateRequestSchema, db: Session) -> schemas.PointCreateResponseSchema:
    """Create Point"""
    if not request.user_id or not request.point_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id, point details per hour are required")
    
    if not request.point_details.amount or not request.point_details.extra_profit_per_hour:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount and extra profit per hour are required")
    
    try:
        point = db.query(PointModel).filter(PointModel.user_id == request.user_id).first()

        if point:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Point already exists")

        new_point = PointModel(
            user_id=request.user_id,
            amount=request.point_details.amount,
            extra_profit_per_hour=request.point_details.extra_profit_per_hour,
            custom_logs=request.point_details.custom_logs,
        )

        db.add(new_point)
        db.commit()
        db.refresh(new_point)

        return schemas.PointCreateResponseSchema(
            point_base=schemas.PointDetailsSchema(
                point=schemas.PointScehma(
                    id=new_point.id,
                    amount=new_point.amount,
                    extra_profit_per_hour=new_point.extra_profit_per_hour,
                    created_at=new_point.created_at,
                    updated_at=new_point.updated_at,
                    custom_logs=new_point.custom_logs,
                )
            )
        )
        
    except Exception as e:
        logging.error(f"An error occured: {e}")


def retrieve_point(id: Optional[int], user_id: Optional[int], db: Session) -> schemas.PointRetrievalResponseSchema:
    """Retrieve Point Details from Single User"""
    if not id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Missing id or user_id")
    
    try:
        base_query = db.query(PointModel)
        filters = []
    
        if id is not None: 
            filters.append(PointModel.id == id)

        if user_id is not None:
            filters.append(PointModel.user_id == user_id)

        if filters: 
            existing_point = base_query.filter(*filters).first()
            
            if not existing_point:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Point not found")
            
            return schemas.PointRetrievalResponseSchema(
                point_base=schemas.PointDetailsSchema(
                    user_id=existing_point.user_id,
                    point=schemas.PointScehma(
                        id=existing_point.id,
                        amount=existing_point.amount,
                        extra_profit_per_hour=existing_point.extra_profit_per_hour,
                        created_at=existing_point.created_at,
                        updated_at=existing_point.updated_at,
                        custom_logs=existing_point.custom_logs,
                    ),
                )
            )
    except Exception as e:
        logging.error(f"An error occurred: {e}")  


def retrieve_point_by_user_id(user_id: int, db: Session) -> schemas.PointRetrievalResponseSchema:
    """Retrieve Point Details from Single User by user_id"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is required")
    
    try:
        existing_point = db.query(PointModel).filter(PointModel.id == user_id).first()
    
        if not existing_point:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Point with user id {user_id} not found")
    
        return schemas.PointRetrievalResponseSchema(
            point_base=schemas.PointDetailsSchema(
                user_id=existing_point.user_id,
                point=schemas.PointScehma(
                    id=existing_point.id,
                    amount=existing_point.amount,
                    extra_profit_per_hour=existing_point.extra_profit_per_hour,
                    created_at=existing_point.created_at,
                    updated_at=existing_point.updated_at,
                    custom_logs=existing_point.custom_logs,
                ),
            )
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_point_list(db: Session, user_ids: List[int], skip: int = 0, limit: int = 15) -> List[schemas.PointRetrievalResponseSchema]:
    """Retrieve Points by List from Multiple Users"""
    try:
        if user_ids:
            existing_points = db.query(PointModel).filter(PointModel.user_id.in_(user_ids)).offset(skip).limit(limit).all()
        else:
            existing_points = db.query(PointModel).offset(skip).limit(limit).all()
        
        return [
            schemas.PointRetrievalResponseSchema(
                point_base=schemas.PointDetailsSchema(
                    user_id=ex.user_id,
                    point=schemas.PointScehma(
                        id=ex.id,
                        amount=ex.amount,
                        extra_profit_per_hour=ex.extra_profit_per_hour,
                        created_at=ex.created_at,
                        updated_at=ex.updated_at,
                        custom_logs=ex.custom_logs,
                    ),
                )
            )
            for ex in existing_points
        ]
        
    except Exception as e:
            logging.error(f"An error occurred: {e}")


def update_point(request: schemas.PointUpdateByIdRequestSchema, db: Session) -> schemas.PointUpdateResponseSchema:
    """Update Point"""
    if not request or not request.type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type and request are required")
    
    try:
        existing_point = db.query(PointModel).filter(PointModel.id == request.id).first()

        if not existing_point:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Point with user_id {request.id} not found")

        if request.type == "add":
            if request.point_payload.amount:
                existing_point.amount += request.point_payload.amount
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing amount")
        elif request.type == "minus":
            if request.point_payload.amount:
                existing_point.amount -= request.point_payload.amount
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing amount")
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method not allowed")    

        if request.point_payload.extra_profit_per_hour:
            existing_point.extra_profit_per_hour = request.point_payload.extra_profit_per_hour

        db.commit()
        db.refresh(existing_point)
        
        return schemas.PointUpdateResponseSchema(
            point_base=schemas.PointDetailsSchema(
                point=schemas.PointScehma(
                    id=existing_point.id,
                    amount=existing_point.amount,
                    extra_profit_per_hour=existing_point.extra_profit_per_hour,
                    created_at=existing_point.created_at,
                    updated_at=existing_point.updated_at,
                    custom_logs=existing_point.custom_logs,
                ),
            user_id=existing_point.user_id
            )
        )
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def delete_point(id: int, db:Session):
    """Delete Point"""
    try:
        db_point = db.query(PointModel).filter(PointModel.id == id).first()
        
        if db_point:
            db.delete(db_point)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Point {id} not found")
        
    except Exception as e:
        logging.error(f"An error occured: {e}")

    

# REVIEW: delete_point, batch update
