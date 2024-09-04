"""Actvity App Business Logics"""

import logging
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.activity import schemas
from app.activity.models import ActivityModel

def create_activity(request: schemas.ActivityCreateRequestSchema, db:Session) -> schemas.ActivityCreateResponseSchema:
    """Create Activity"""
    if not request.user_id or not request.activity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID and activity are required")

    try:
        db_activity = db.query(ActivityModel).filter(ActivityModel.user_id==request.user_id).first()

        if db_activity:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Activity already exists")

        new_activity=ActivityModel(
            user_id=request.user_id,
            is_logged_in=True,
            login_streak=0,
            total_logins=0,
            last_action_time=datetime.now(),
            last_login_time=datetime.now(),
            custom_logs=request.activity.custom_logs
        )

        db.add(new_activity)
        db.commit()
        db.refresh(new_activity)

        return schemas.ActivityCreateResponseSchema(
            user_id=new_activity.user_id,
            activity=schemas.ActivityBaseSchema(
                id=new_activity.id,
                is_logged_in=new_activity.is_logged_in,
                login_streak=new_activity.login_streak,
                total_logins=new_activity.total_logins,
                last_action_time=new_activity.last_action_time,
                last_login_time=new_activity.last_login_time,
                custom_logs=new_activity.custom_logs,
                updated_at=new_activity.updated_at,
                created_at=new_activity.created_at
            )
        )

    except Exception as e:
        logging.error(f"An error occured: {e}")

    
def retrieve_activity(id:Optional[int], user_id:Optional[int], db: Session) -> schemas.ActivityRetrievalResponseSchema:
    """Retrieve Activity Details from Single User"""
    if not id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id or user_id")

    try:
        base_query = db.query(ActivityModel)
        filters = []

        if id is not None:
            filters.append(ActivityModel.id==id)

        if user_id is not None:
            filters.append(ActivityModel.user_id==user_id)

        if filters:
            existing_activity = base_query.filter(*filters).first()

            if not existing_activity:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Activity not found")
            
            return schemas.ActivityRetrievalResponseSchema(
                user_id=existing_activity.user_id,
                activity=schemas.ActivityBaseSchema(
                    id=existing_activity.id,
                    is_logged_in=existing_activity.is_logged_in,
                    login_streak=existing_activity.login_streak,
                    total_logins=existing_activity.total_logins,
                    last_action_time=existing_activity.last_action_time,
                    last_login_time=existing_activity.last_login_time,
                    created_at=existing_activity.created_at,
                    updated_at=existing_activity.updated_at,
                    custom_logs=existing_activity.custom_logs
                )
            )
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def retrieve_activity_list(db: Session, user_ids: List[int], skip: int = 0, limit: int = 15) -> List[schemas.ActivityRetrievalResponseSchema]:
    """Retrieve Activities by List from Multiple Users"""
    try:
        if user_ids:
            existing_activities = db.query(ActivityModel).filter(ActivityModel.user_id.in_(user_ids)).offset(skip).limit(limit).all()
        else:
            existing_activities = db.query(ActivityModel).offset(skip).limit(limit).all()
            
        return [
            schemas.ActivityRetrievalResponseSchema(
                user_id=existing_activity.user_id,
                activity=schemas.ActivityBaseSchema(
                    id=existing_activity.id,
                    is_logged_in=existing_activity.is_logged_in,
                    login_streak=existing_activity.login_streak,
                    total_logins=existing_activity.total_logins,
                    last_action_time=existing_activity.last_action_time,
                    last_login_time=existing_activity.last_login_time,
                    created_at=existing_activity.created_at,
                    updated_at=existing_activity.updated_at,
                    custom_logs=existing_activity.custom_logs
                )
            )
            for existing_activity in existing_activities
        ]
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def update_activity(request: schemas.ActivityUpdateRequestSchema, db: Session) -> schemas.ActivityUpdateResponseSchema:
    """Update Activity"""
    if not request or not request.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id")
    
    try:
        existing_activity = db.query(ActivityModel).filter(ActivityModel.id==request.id).first()
        
        if not existing_activity:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Activity not found")
        
        if request.activity:
            for field, value in request.activity.model_dump(exclude_unset=True).items():
                if hasattr(existing_activity, field):
                    setattr(existing_activity, field, value)
        
        db.commit()
        db.refresh(existing_activity)
        
        return schemas.ActivityUpdateResponseSchema(
            user_id=existing_activity.user_id,
            activity=schemas.ActivityBaseSchema(
                id=existing_activity.id,
                is_logged_in=existing_activity.is_logged_in,
                login_streak=existing_activity.login_streak,
                total_logins=existing_activity.total_logins,
                last_action_time=existing_activity.last_action_time,
                last_login_time=existing_activity.last_login_time,
                created_at=existing_activity.created_at,
                updated_at=existing_activity.updated_at,
                custom_logs=existing_activity.custom_logs
            )
        )
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def delete_activity(id: int, db: Session):
    """Delete Activity"""
    try:
        db_activity = db.query(ActivityModel).filter(ActivityModel.id == id).first()
        
        if db_activity:
            db.delete(db_activity)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Activity {id} not found")
        
    except Exception as e:
        logging.error(f"An error occured: {e}")

    
#TODO: get by date range