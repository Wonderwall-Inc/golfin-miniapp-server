"""Point App Business Logics"""

import logging
from typing import List, Optional
from sqlalchemy import desc, func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.point import schemas
from app.point.models import PointModel

def create_point(request: schemas.PointCreateRequestSchema, db: Session) -> schemas.PointCreateResponseSchema:
    """Create Point"""
    if not request.user_id or not request.point_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id, point details per hour are required")
    
    # if not request.point_details.amount or not request.point_details.extra_profit_per_hour:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount and extra profit per hour are required")
    
    try:
        point = db.query(PointModel).filter(PointModel.user_id == request.user_id).first()

        if point:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Point already exists")

        new_point = PointModel(
            user_id=request.user_id,
            login_amount=request.point_details.login_amount,
            referral_amount=request.point_details.referral_amount,
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
                    login_amount=new_point.login_amount,
                    referral_amount=new_point.referral_amount,
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
                        login_amount=existing_point.login_amount,
                        referral_amount=existing_point.referral_amount,
                        extra_profit_per_hour=existing_point.extra_profit_per_hour,
                        created_at=existing_point.created_at,
                        updated_at=existing_point.updated_at,
                        custom_logs=existing_point.custom_logs,
                    ),
                )
            )
    except Exception as e:
        logging.error(f"An error occurred: {e}")  

def get_point_ranking(id: Optional[int], user_id: Optional[int], db: Session) -> int:
    """Retrieve Point Details from Single User"""
    if not id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Missing id or user_id")
    
    try:
        # base_query = db.query(PointModel)
        #filters = []
        subquery = db.query(
            PointModel.id,
            PointModel.user_id,
            (PointModel.login_amount + PointModel.referral_amount).label('total_points'),
            func.rank().over(order_by=desc('total_points')).label('rank')
        ).subquery()
        
        query = db.query(subquery.c.rank)
        
        if id is not None: 
            query.filter(subquery.c.id == id)

        if user_id is not None:
            query.filter(subquery.c.user_id == user_id)

        rank = query.scalar()
        print('rank', rank)
        
        if rank is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Point not found")
        return rank
        #if filters: 
        #    rank = query.scalar()
        #    return rank
            # if not existing_point:
            #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Point not found")
            
            # return schemas.PointRetrievalResponseSchema(
            #     point_base=schemas.PointDetailsSchema(
            #         user_id=existing_point.user_id,
            #         point=schemas.PointScehma(
            #             id=existing_point.id,
            #             login_amount=existing_point.login_amount,
            #             referral_amount=existing_point.referral_amount,
            #             extra_profit_per_hour=existing_point.extra_profit_per_hour,
            #             created_at=existing_point.created_at,
            #             updated_at=existing_point.updated_at,
            #             custom_logs=existing_point.custom_logs,
            #         ),
            #     )
            # )
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
                    login_amount=existing_point.login_amount,
                    referral_amount=existing_point.referral_amount,
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
                        login_amount=ex.login_amount,
                        referral_amount=ex.referral_amount,
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
            if request.point_payload.login_amount:
                existing_point.login_amount += request.point_payload.login_amount
            if request.point_payload.referral_amount:
                existing_point.referral_amount += request.point_payload.referral_amount
            if request.point_payload.extra_profit_per_hour: # can be add or minus for that
                existing_point.extra_profit_per_hour += request.point_payload.extra_profit_per_hour

        elif request.type == "minus":
            if request.point_payload.login_amount:
                existing_point.login_amount -= request.point_payload.login_amount
            if request.point_payload.login_amount:
                existing_point.referral_amount -= request.point_payload.referral_amount
            if request.point_payload.extra_profit_per_hour: # can be add or minus for that
                existing_point.extra_profit_per_hour -= request.point_payload.extra_profit_per_hour
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method not allowed")    

    
        db.commit()
        db.refresh(existing_point)
        
        return schemas.PointUpdateResponseSchema(
            point_base=schemas.PointDetailsSchema(
                point=schemas.PointScehma(
                    id=existing_point.id,
                    login_amount=existing_point.login_amount,
                    referral_amount=existing_point.referral_amount,
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
