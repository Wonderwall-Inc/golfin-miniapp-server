import logging
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.activity import schemas
from app.activity.models import ActivityModel
from datetime import datetime

def create_activity(request: schemas.ActivityCreateRequestSchema, db:Session) -> schemas.ActivityCreateResponseSchema:
    if not request.user_id or not request.activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID and activity are required"
        )

    db_activity = db.query(ActivityModel).filter(ActivityModel.user_id==request.user_id).first()
    
    if db_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Activity already exists"
        )
    
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

    
def retrieve_activity(id:Optional[int], user_id:Optional[int], db: Session) -> schemas.ActivityRetrievalResponseSchema:
    if id is None and user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id or user_id")

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
        try:
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

def retrieve_activity_list(user_ids: List[int], db: Session) -> List[schemas.ActivityRetrievalResponseSchema]:
    return 

def update_activity(request: schemas.ActivityUpdateRequestSchema, db: Session) -> schemas.ActivityUpdateResponseSchema:
    return

def delete_activity():
    return

#TODO: get by date range