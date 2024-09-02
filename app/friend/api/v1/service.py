import logging
from typing import List
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from app.friend.models import FriendModel
from app.user.models import UserModel
from app.friend.schemas import (
    FriendStatusTpye,
    FriendBaseSchema,
    FriendUpdateDetailsSchema,
    FriendSchema,
    FriendIds,
    FriendWithIdsRetrivalResponseSchema,
    FriendDetailsSchema,
    FriendCreateRequestSchema,
    FriendCreateResponseSchema,
    FriendRetrivalRequestSchema,
    FriendRetrivalResponseSchema,
    # FriendUpdateRequestSchema,
    FriendDetailsResponseSchema,
    FriendUpdateByIdRequestSchema,
    FriendUpdateBySenderIdRequestSchema,
    FriendUpdateByReceiverIdRequestSchema,
)
from app.user.schemas import UserSchema

# from core.utils import GameCharacterSchemaFactory


def create_friend(
    request: FriendCreateRequestSchema, db: Session
) -> FriendCreateResponseSchema:
    """Create New Friendship"""

    if not request.sender_id or not request.receiver_id or not request.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sender id, receiver id and status are required",
        )

    # Check if the sender id as sender or receiver on the friend table
    sender_id_as_sender = (
        db.query(FriendModel).filter(FriendModel.sender_id == request.sender_id).first()
    )

    sender_id_as_receiver = (
        db.query(FriendModel)
        .filter(FriendModel.receiver_id == request.sender_id)
        .first()
    )

    # Check if receiver id as sender or receiver on the friend table
    receiver_id_as_sender = (
        db.query(FriendModel)
        .filter(FriendModel.sender_id == request.receiver_id)
        .first()
    )

    receiver_id_as_receiver = db.query(FriendModel).filter(
        FriendModel.receiver_id == request.receiver_id
    )
    if not (sender_id_as_sender is None and receiver_id_as_receiver is None) or not (
        sender_id_as_receiver is None and receiver_id_as_sender is None
    ):
        new_friend = FriendModel(
            sender_id=request.sender_id,
            receiver_id=request.receiver_id,
            status=request.status,
        )
        db.add(new_friend)
        db.commit()
        db.refresh(new_friend)
        return FriendCreateResponseSchema(
            friend_details=FriendDetailsSchema(
                friend_base=FriendSchema(
                    id=new_friend.id,
                    status=new_friend.status,
                    created_at=new_friend.created_at,
                    updated_at=new_friend.updated_at,
                    custom_logs=new_friend.custom_logs,
                ),
                sender_id=new_friend.sender_id,
                receiver_id=new_friend.receiver_id,
            )
        )
    else:
        return None


# This method combines with get_friends_as_receiver ->> total friend from the given user_id
def get_friends_as_sender(
    user_id: int, db: Session
) -> List[FriendRetrivalResponseSchema]:
    """Retrieve friend by sender id"""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing User id"
        )
    friends = (
        db.query(UserModel)
        .join(
            FriendModel,
            (UserModel.id == FriendModel.sender_id)
            and (FriendModel.sender_id == user_id),
        )
        .all()
    )
    return [
        FriendRetrivalResponseSchema(
            friend_details=FriendDetailsSchema(
                friend_base=FriendSchema(
                    id=friend.sender.id,
                    status=friend.sender.status,
                    created_at=friend.sender.created_at,
                    updated_at=friend.sender.updated_at,
                    custom_logs=friend.sender.custom_logs,
                ),
                sender_id=friend.sender.sender_id,
                receiver_id=friend.sender.receiver_id,
            )
        )
        for friend in friends
    ]


# This method combines with get_friends_as_sender ->> total friend from the given user_id
def get_friends_as_receiver(
    user_id: int, db: Session
) -> List[FriendRetrivalResponseSchema]:
    """Retrieve friend by sender id"""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing User id"
        )
    friends = (
        db.query(UserModel)
        .join(
            FriendModel,
            (UserModel.id == FriendModel.sender_id)
            and (FriendModel.sender_id == user_id),
        )
        .all()
    )
    return [
        FriendRetrivalResponseSchema(
            friend_details=FriendDetailsSchema(
                friend_base=FriendSchema(
                    id=friend.receiver.id,
                    status=friend.receiver.status,
                    created_at=friend.receiver.created_at,
                    updated_at=friend.receiver.updated_at,
                    custom_logs=friend.receiver.custom_logs,
                ),
                sender_id=friend.receiver.sender_id,
                receiver_id=friend.receiver.receiver_id,
            )
        )
        for friend in friends
    ]


def retrieve_friend_by_id(
    request: FriendRetrivalRequestSchema, db: Session
) -> FriendRetrivalResponseSchema:
    if not request.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing friend id"
        )
    friend = db.query(FriendModel).filter(FriendModel.id == id).first()
    return FriendRetrivalResponseSchema(
        friend_details=FriendDetailsSchema(
            friend_base=FriendSchema(
                id=friend.id,
                status=friend.status,
                created_at=friend.created_at,
                updated_at=friend.updated_at,
                custom_logs=friend.custom_logs,
            ),
            sender_id=friend.sender_id,
            receiver_id=friend.receiver_id,
        )
    )


def retrieve_friends_by_user_id(
    user_id: int,
    db: Session,
) -> FriendWithIdsRetrivalResponseSchema:
    """Retrieve Friend by user id"""
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing User id"
        )
    as_sender = db.query(FriendModel).filter(FriendModel.sender_id == user_id).all()
    as_receiver = db.query(FriendModel).filter(FriendModel.receiver_id == user_id).all()
    as_sender_list = [
        FriendBaseSchema(
            id=friend_from_as_sender.id,
            sender_id=friend_from_as_sender.sender_id,
            receiver_id=friend_from_as_sender.receiver_id,
            created_at=friend_from_as_sender.created_at,
            updated_at=friend_from_as_sender.updated_at,
            status=friend_from_as_sender.status,
        )
        for friend_from_as_sender in as_sender
    ]
    as_receiver_list = [
        FriendBaseSchema(
            id=friend_from_as_receiver.id,
            sender_id=friend_from_as_receiver.sender_id,
            receiver_id=friend_from_as_receiver.receiver_id,
            created_at=friend_from_as_receiver.created_at,
            updated_at=friend_from_as_receiver.updated_at,
            status=friend_from_as_receiver.status,
        )
        for friend_from_as_receiver in as_receiver
    ]

    # return as_sender_list, as_receiver_list
    return FriendWithIdsRetrivalResponseSchema(
        sender=as_sender_list, receiver=as_receiver_list
    )


def get_Friend_by_sender_id_receiver_id(
    sender_id: int, db: Session, receiver_id: int
) -> FriendRetrivalResponseSchema:
    if not sender_id or not receiver_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing sender id or receiver id",
        )
    existing_friend = (
        db.query(FriendModel)
        .filter(
            FriendModel.sender_id == sender_id,
            FriendModel.receiver_id == receiver_id,
        )
        .first()
    )
    return FriendRetrivalResponseSchema(
        friend_details=FriendDetailsSchema(
            friend_base=FriendSchema(
                id=existing_friend.id,
                status=existing_friend.status,
                created_at=existing_friend.created_at,
                updated_at=existing_friend.updated_at,
                custom_logs=existing_friend.custom_logs,
            ),
            sender_id=existing_friend.sender_id,
            receiver_id=existing_friend.receiver_id,
        )
    )


# by friend id only
def update_friend_status_by_friend_id(
    request: FriendUpdateByIdRequestSchema,
    db: Session,
) -> FriendDetailsResponseSchema:
    """Update single friend by friend id"""
    if not request.id or not request.friend_payload.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Friend id and status are required",
        )
    db_friend = db.query(FriendModel).filter(FriendModel.id == request.id).first()
    if db_friend:
        if request.friend_payload.status:
            db_friend.status = request.friend_payload.status
        if request.friend_payload.custom_logs:
            db_friend.custom_logs = request.friend_payload.custom_logs
        db.commit()
        db.refresh(db_friend)
    return FriendDetailsResponseSchema(
        friend_details=FriendDetailsSchema(
            friend_base=FriendSchema(
                id=db_friend.id,
                status=db_friend.status,
                created_at=db_friend.created_at,
                updated_at=db_friend.updated_at,
                custom_logs=db_friend.custom_logs,
            ),
            sender_id=db_friend.sender_id,
            receiver_id=db_friend.receiver_id,
        )
    )


# FIXME: support multiple later on
def update_friend_status_by_sender_id(
    request: FriendUpdateBySenderIdRequestSchema,
    db: Session,
) -> FriendDetailsResponseSchema:
    """Update single friend by sender id"""
    if not request.sender_id or not request.friend_payload.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Friend sender id and status are required",
        )
    db_friend = (
        db.query(FriendModel).filter(FriendModel.sender_id == request.sender_id).first()
    )
    if db_friend:
        if request.friend_payload.status:
            db_friend.status = request.friend_payload.status
        if request.friend_payload.custom_logs:
            db_friend.custom_logs = request.friend_payload.custom_logs
        db.commit()
        db.refresh(db_friend)
    return FriendDetailsResponseSchema(
        friend_details=FriendDetailsSchema(
            friend_base=FriendSchema(
                id=db_friend.id,
                status=db_friend.status,
                created_at=db_friend.created_at,
                updated_at=db_friend.updated_at,
                custom_logs=db_friend.custom_logs,
            ),
            sender_id=db_friend.sender_id,
            receiver_id=db_friend.receiver_id,
        )
    )


# FIXME: support multiple later on
def update_friend_status_by_receiver_id(
    request: FriendUpdateByReceiverIdRequestSchema,
    db: Session,
) -> FriendDetailsResponseSchema:
    """Update single friend by receiver id"""
    if not request.receiver_id or not request.friend_payload.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Friend receiver id and status are required",
        )
    db_friend = (
        db.query(FriendModel)
        .filter(FriendModel.receiver_id == request.receiver_id)
        .first()
    )
    if db_friend:
        if request.friend_payload.status:
            db_friend.status = request.friend_payload.status
        if request.friend_payload.custom_logs:
            db_friend.custom_logs = request.friend_payload.custom_logs
        db.commit()
        db.refresh(db_friend)
    return FriendDetailsResponseSchema(
        friend_details=FriendDetailsSchema(
            friend_base=FriendSchema(
                id=db_friend.id,
                status=db_friend.status,
                created_at=db_friend.created_at,
                updated_at=db_friend.updated_at,
                custom_logs=db_friend.custom_logs,
            ),
            sender_id=db_friend.sender_id,
            receiver_id=db_friend.receiver_id,
        )
    )


def batch_update_by_user_id_to_receiver():
    pass


def remove_friend(
    sender_id: int,
    receiver_id: int,
    db: Session,
):
    friendship = get_Friend_by_sender_id_receiver_id(sender_id, db, receiver_id)
    if friendship:
        db.delete(friendship)
        db.commit()
    else:
        raise ValueError("Friendship not found")
