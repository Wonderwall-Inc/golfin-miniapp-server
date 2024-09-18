"""Friend App Business Logics"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.friend import schemas
from app.user.models import UserModel
from app.friend.models import FriendModel

def create_friend(request: schemas.FriendCreateRequestSchema, db: Session) -> schemas.FriendCreateResponseSchema :
    """Create Friend"""
    print('create friend request')
    print(request)
    if not request.sender_id or not request.receiver_id or not request.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sender id, receiver id and status are required")

    # Check if the sender id as sender or receiver on the friend table
    # sender_id_as_sender = db.query(FriendModel).filter(FriendModel.sender_id == request.sender_id).first()
    # sender_id_as_receiver = db.query(FriendModel).filter(FriendModel.receiver_id == request.sender_id).first()

    # # Check if receiver id as sender or receiver on the friend table
    # receiver_id_as_sender = db.query(FriendModel).filter(FriendModel.sender_id == request.receiver_id).first()
    # receiver_id_as_receiver = db.query(FriendModel).filter(FriendModel.receiver_id == request.receiver_id).first


    all_friends = db.query(FriendModel).all()
    
    for friend in all_friends:
        if friend.sender_id is request.sender_id and friend.receiver_id is request.receiver_id:
            print('case 1')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender and receiver existed") 
        if friend.sender_id is request.receiver_id and friend.receiver_id is request.sender_id:
            print('case 2')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender and receiver existed") 
    
    new_friend = FriendModel(
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        status=request.status,
    )
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return schemas.FriendCreateResponseSchema(
        friend_details=schemas.FriendDetailsSchema(
            friend_base=schemas.FriendSchema(
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
    # if not (sender_id_as_sender is None and receiver_id_as_receiver is None) or not (sender_id_as_receiver is None and receiver_id_as_sender is None):
    if sender_id_as_sender and sender_id_as_receiver:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender and receiver existed") 
    
    if receiver_id_as_sender and receiver_id_as_receiver:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="sender and receiver existed") 
    
   


# This method combines with get_friends_as_receiver ->> total friend from the given user_id
def get_friends_as_sender(user_id: int, db: Session) -> List[schemas.FriendRetrievalResponseSchema]:
    """Retrieve friend by sender id"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing User id")

    friends = db.query(UserModel).join(FriendModel, (UserModel.id == FriendModel.sender_id) and (FriendModel.sender_id == user_id)).all()
    return [
        schemas.FriendRetrievalResponseSchema(
            friend_details=schemas.FriendDetailsSchema(
                friend_base=schemas.FriendSchema(
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
def get_friends_as_receiver(user_id: int, db: Session) -> List[schemas.FriendRetrievalResponseSchema]:
    """Retrieve friend by sender id"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing User id")

    friends = db.query(UserModel).join(FriendModel, (UserModel.id == FriendModel.sender_id) and (FriendModel.sender_id == user_id)).all()

    return [
        schemas.FriendRetrievalResponseSchema(
            friend_details=schemas.FriendDetailsSchema(
                friend_base=schemas.FriendSchema(
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

# FIXME
def retrieve_friends(id: Optional[int], user_id: Optional[int], db: Session) -> schemas.FriendWithIdsRetrievalResponseSchema:
    """Retrieve Friend Details from Single User"""
    print('retrieve friends request')
    print('id:', id )
    print('user_id:', user_id)

    if not id and not user_id: # avoid both none on optional case
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id or user_id")

    try:
        sender_query = db.query(FriendModel)
        receiver_query = db.query(FriendModel)
        
        sender_filters = []
        receiver_filters = []
        
        if id is not None:
            sender_filters.append(FriendModel.id == id)
            receiver_filters.append(FriendModel.id == id)

        if user_id is not None:
            # filters.append((FriendModel.sender_id == user_id)|(FriendModel.receiver_id == user_id))
            sender_filters.append(FriendModel.sender_id == user_id)
            receiver_filters.append(FriendModel.receiver_id == user_id)
            
            
        if sender_filters and receiver_filters:
            existing_sender = sender_query.filter(*sender_filters).all()
            existing_receiver = receiver_query.filter(*receiver_filters).all()
            
            sender = [
                schemas.FriendBaseSchema(
                    id=fs.id,
                    sender_id=fs.sender_id,
                    receiver_id=fs.receiver_id,
                    created_at=fs.created_at,
                    updated_at=fs.updated_at,
                    status=fs.status,
                )
                for fs in existing_sender
            ]
            
            receiver = [
                schemas.FriendBaseSchema(
                    id=fr.id,
                    sender_id=fr.sender_id,
                    receiver_id=fr.receiver_id,
                    created_at=fr.created_at,
                    updated_at=fr.updated_at,
                    status=fr.status,
                )
                for fr in existing_receiver
            ]
            return schemas.FriendWithIdsRetrievalResponseSchema(sender=sender,receiver=receiver)
               
    except Exception as e:
        logging.error(f"An error occured: {e}")


def retrieve_friend_list(db: Session, user_ids: List[int], skip: int = 0, limit: int = 15) -> schemas.FriendWithIdsRetrievalResponseSchema:
    """Retrieve Friends by List from Multiple Users"""
    try:
        if user_ids:
            existing_friends_as_sender = db.query(FriendModel).filter(FriendModel.sender_id.in_(user_ids)).offset(skip).limit(limit).all()
            existing_friends_as_receiver = db.query(FriendModel).filter(FriendModel.receiver_id.in_(user_ids)).offset(skip).limit(limit).all()
            as_sender_list = [
            schemas.FriendBaseSchema(
                id=friend_from_as_sender.id,
                sender_id=friend_from_as_sender.sender_id,
                receiver_id=friend_from_as_sender.receiver_id,
                created_at=friend_from_as_sender.created_at,
                updated_at=friend_from_as_sender.updated_at,
                status=friend_from_as_sender.status,
            )
            for friend_from_as_sender in existing_friends_as_sender
            ]

            as_receiver_list = [
            schemas.FriendBaseSchema(
                id=friend_from_as_receiver.id,
                sender_id=friend_from_as_receiver.sender_id,
                receiver_id=friend_from_as_receiver.receiver_id,
                created_at=friend_from_as_receiver.created_at,
                updated_at=friend_from_as_receiver.updated_at,
                status=friend_from_as_receiver.status,
            )
            for friend_from_as_receiver in existing_friends_as_receiver
            ]

            return schemas.FriendWithIdsRetrievalResponseSchema(
                sender=as_sender_list, receiver=as_receiver_list
            )

        else:
            existing_friends =  db.query(FriendModel).offset(skip).limit(limit).all()

            as_sender = []
            as_receiver = []

            for friend in existing_friends:
                if friend.sender and len(friend.sender):
                    as_sender.append(
                        schemas.FriendBaseSchema(
                            id=friend.id,
                            sender_id=friend.sender_id,
                            receiver_id=friend.receiver_id,
                            created_at=friend.created_at,
                            updated_at=friend.updated_at,
                            status=friend.status
                        )
                    )
                if friend.receiver and len(friend.receiver):
                    as_receiver.append(
                        schemas.FriendBaseSchema(
                            id=friend.id,
                            sender_id=friend.sender_id,
                            receiver_id=friend.receiver_id,
                            created_at=friend.created_at,
                            updated_at=friend.updated_at,
                            status=friend.status
                        )
                    )

            return schemas.FriendWithIdsRetrievalResponseSchema(
                sender=as_sender, receiver=as_receiver
            )

        # return as_sender_list, as_receiver_list

    except Exception as e:
        logging.error(f"An error occured: {e}")


def get_Friend_by_sender_id_receiver_id(sender_id: int, db: Session, receiver_id: int) -> schemas.FriendRetrievalResponseSchema:
    if not sender_id or not receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Missing sender id or receiver id")

    existing_friend = db.query(FriendModel).filter(FriendModel.sender_id == sender_id, FriendModel.receiver_id == receiver_id).first()

    return schemas.FriendRetrievalResponseSchema(
        friend_details=schemas.FriendDetailsSchema(
            friend_base=schemas.FriendSchema(
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
def update_friend(id: Optional[int], sender_id: Optional[int], receiver_id: Optional[int], friend_status: str, custom_logs: Optional[dict], db: Session) -> List[schemas.FriendDetailsResponseSchema]:
    """Update single friend by friend id"""
    if not id and not sender_id and not receiver_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing id or sender id or receiver id")

    if not friend_status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing status")

    try:
        base_query = db.query(FriendModel)
        filters = []

        if id:
            filters.append(FriendModel.id==id)

        if sender_id:
            filters.append(FriendModel.sender_id==sender_id)

        if receiver_id:
            filters.append(FriendModel.receiver_id==receiver_id)

        if filters:
            existing_friends = base_query.filter(*filters).all()

            if not existing_friends:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend not found")

            for friend in existing_friends:
                friend.status = friend_status
                friend.custom_logs = custom_logs
                db.commit()
                db.refresh(friend)

            return [
                schemas.FriendDetailsResponseSchema(
                friend_details=schemas.FriendDetailsSchema(
                    friend_base=schemas.FriendSchema(
                        id=f.id,
                        status=f.status,
                        created_at=f.created_at,
                        updated_at=f.updated_at,
                        custom_logs=f.custom_logs,
                    ),
                    sender_id=f.sender_id,
                    receiver_id=f.receiver_id,
                )
            )
                for f in existing_friends
            ]
    except Exception as e:
        logging.error(f"An error occured: {e}")

# FIXME: support multiple later on
def update_friend_status_by_sender_id(request: schemas.FriendUpdateBySenderIdRequestSchema, db: Session) -> schemas.FriendDetailsResponseSchema:
    """Update single friend by sender id"""
    if not request.sender_id or not request.friend_payload.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Friend sender id and status are required")

    db_friend = db.query(FriendModel).filter(FriendModel.sender_id == request.sender_id).first()

    if db_friend:
        if request.friend_payload.status:
            db_friend.status = request.friend_payload.status
        if request.friend_payload.custom_logs:
            db_friend.custom_logs = request.friend_payload.custom_logs

        db.commit()
        db.refresh(db_friend)

    return schemas.FriendDetailsResponseSchema(
        friend_details=schemas.FriendDetailsSchema(
            friend_base=schemas.FriendSchema(
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
def update_friend_status_by_receiver_id(request: schemas.FriendUpdateByReceiverIdRequestSchema, db: Session) -> schemas.FriendDetailsResponseSchema:
    """Update single friend by receiver id"""
    if not request.receiver_id or not request.friend_payload.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Friend receiver id and status are required")

    db_friend = db.query(FriendModel).filter(FriendModel.receiver_id == request.receiver_id).first()

    if not db_friend:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Friend receiver_id {request.receiver_id} not found")

    if db_friend:
        if request.friend_payload.status:
            db_friend.status = request.friend_payload.status
        if request.friend_payload.custom_logs:
            db_friend.custom_logs = request.friend_payload.custom_logs

        db.commit()
        db.refresh(db_friend)

    return schemas.FriendDetailsResponseSchema(
        friend_details=schemas.FriendDetailsSchema(
            friend_base=schemas.FriendSchema(
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


def remove_friend(sender_id: int, receiver_id: int, db: Session):
    friendship = get_Friend_by_sender_id_receiver_id(sender_id, db, receiver_id)
    if friendship:
        db.delete(friendship)
        db.commit()
    else:
        raise ValueError("Friendship not found")
