"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.friend import schemas
from app.friend.api.v1 import service


router = APIRouter(prefix="/api/v1/friend", tags=["friend"])
get_db = database.get_db


# REVIEW: create & create + get from use & create + get from users
@router.post("/create", response_model=schemas.FriendCreateResponseSchema)
def create_friend(
    request: schemas.FriendCreateRequestSchema,
    db: Session = Depends(get_db),
):
    """create friendship"""
    return service.create_friend(request, db)


# REVIEW:  get from user & get from users
@router.get("/details/{user_id}", response_model=schemas.FriendWithIdsRetrivalResponseSchema)
def get_friend(user_id: int, db: Session = Depends(get_db)):
    """get friendship"""
    return service.retrieve_friends_by_user_id(user_id, db)


@router.put("/details/id", response_model=schemas.FriendDetailsResponseSchema)
def update_friend_status_by_user_id(
    request: schemas.FriendUpdateByIdRequestSchema, db: Session = Depends(get_db)
):
    """update status of friendship based on id"""
    return service.update_friend_status_by_friend_id(request, db)


@router.put("/details/sender", response_model=schemas.FriendDetailsResponseSchema)
def update_friend_status_by_sender_id(
    request: schemas.FriendUpdateBySenderIdRequestSchema, db: Session = Depends(get_db)
):
    """update status of friendship based on sender id"""
    return service.update_friend_status_by_sender_id(request, db)


@router.put("/details/receiver", response_model=schemas.FriendDetailsResponseSchema)
def update_friend_status_by_receiver_id(
    request: schemas.FriendUpdateByReceiverIdRequestSchema,
    db: Session = Depends(get_db),
):
    """update status of friendship based on receiver id"""
    return service.update_friend_status_by_receiver_id(request, db)


# TODO: update the status by sender and receiver id
