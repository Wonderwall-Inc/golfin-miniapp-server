"""Friend App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from core import database
from app.friend import schemas
from app.friend.api.v1 import service

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

get_db = database.get_db

router = APIRouter(prefix="/api/v1/friend", tags=["friend"])


# REVIEW: create & create + get from use & create + get from users
@router.post("/create", response_model=schemas.FriendCreateResponseSchema)
def create_friend(request: schemas.FriendCreateRequestSchema, db: Session = Depends(get_db)):
    """Create friend"""
    return service.create_friend(request, db)


# REVIEW:  get from user & get from users
@router.get("/detail", response_model=schemas.FriendWithIdsRetrievalResponseSchema)
def get_friend_from_user(id: Optional[int] = None, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retrieve Friend Details from Single User"""
    result = service.retrieve_friends(id, user_id, db)
    print('result')
    print(result)
    json_compatible_item_data = jsonable_encoder(service.retrieve_friends(id, user_id, db))
    return JSONResponse(content=json_compatible_item_data)

# REVIEW:  get from user & get from users
@router.get("/details", response_model=schemas.FriendWithIdsRetrievalResponseSchema)
def get_friend_from_users(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve Friend by List from Multiple Users"""
    return service.retrieve_friend_list(db, user_ids, skip, limit)


@router.put("/update", response_model=List[schemas.FriendDetailsResponseSchema])
def update_friend(friend_status: str, id: Optional[int] = None, sender_id: Optional[int] = None, receiver_id: Optional[int] = None, custom_logs: Optional[dict] = None, db: Session = Depends(get_db)):
    """Update Status"""
    return service.update_friend(id, sender_id, receiver_id, friend_status, custom_logs, db)


@router.patch("/reward-update", response_model=List[schemas.FriendDetailsResponseSchema])
def batch_update_reward_claimed_by_sender_id(sender_ids: List[int] = Query(default=None), db: Session = Depends(get_db)):
    """Update multiple friend has_claimed by list of sender id"""
    return service.batch_update_reward_claimed_by_sender_id(db, sender_ids)
