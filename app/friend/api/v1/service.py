"""Friend App Business Logics"""

import logging
from typing import List, Optional
from sqlalchemy import desc, distinct, func, literal, union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.friend import schemas
from app.user.models import UserModel
from app.friend.models import FriendModel

def create_friend(request: schemas.FriendCreateRequestSchema, db: Session) -> schemas.FriendCreateResponseSchema:
    """Create Friend"""
    print('create friend request')
    print(request)

    if not request.sender_id or not request.receiver_id or not request.status:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sender id, receiver id and status are required")

    # Check for existing friendship (more efficient approach)
    existing_friend = db.query(FriendModel).filter(
        ((FriendModel.sender_id == request.sender_id) & (FriendModel.receiver_id == request.receiver_id)) |
        ((FriendModel.sender_id == request.receiver_id) & (FriendModel.receiver_id == request.sender_id))
    ).first()

    if existing_friend:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Friend relationship already exists")

    # Create new friend if no existing relationship
    new_friend = FriendModel(
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        status=request.status,
        has_claimed=request.has_claimed,
    )
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)

    return schemas.FriendCreateResponseSchema(
        friend_details=schemas.FriendDetailsSchema(
            friend_base=schemas.FriendSchema(
                id=new_friend.id,
                status=new_friend.status,
                has_claimed=new_friend.has_claimed,
                created_at=new_friend.created_at,
                updated_at=new_friend.updated_at,
                custom_logs=new_friend.custom_logs,
            ),
            sender_id=new_friend.sender_id,
            receiver_id=new_friend.receiver_id,
        )
    )


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
                    has_claimed=friend.has_claimed,
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
                    has_claimed=friend.has_claimed,
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
                    has_claimed=fs.has_claimed
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
                    has_claimed=fr.has_claimed
                )
                for fr in existing_receiver
            ]
            return schemas.FriendWithIdsRetrievalResponseSchema(sender=sender,receiver=receiver)
               
    except Exception as e:
        logging.error(f"An error occured: {e}")

from sqlalchemy import func, desc, distinct, literal, union
from sqlalchemy.exc import SQLAlchemyError

def get_referral_ranking(user_id: int, db: Session):
    """Retrieve referral ranking for a user"""
    logging.info(f"get_referral_ranking called with user_id={user_id}")
    
    if not user_id:
        logging.error("Missing user_id")
        referral_count = db.query(
                FriendModel.sender_id,
                func.count(FriendModel.id).label('referral_count'),
                ).group_by(FriendModel.sender_id).subquery()
        all_users = db.query(FriendModel).filter(FriendModel.sender_id == user_id).order_by(desc(func.coalesce(referral_count.c.referral_count, 0))).limit(10).all()
        logging.info(all_users)
        return all_users
    
    else:
        try:
            # Subquery to count referrals for each user
            referral_count = db.query(
                FriendModel.sender_id,
                func.count(FriendModel.id).label('referral_count'),
                ).group_by(FriendModel.sender_id).subquery()
        
            all_users = union(
                db.query(distinct(FriendModel.sender_id)),
                db.query(literal(user_id).label('sender_id'))
            ).alias('all_users')

            # Subquery to rank users based on referral count
            ranking = db.query(
                all_users.c.sender_id.label('user_id'),
                func.coalesce(referral_count.c.referral_count, 0).label('referral_count'),
                func.rank().over(
                    order_by=[
                        desc(func.coalesce(referral_count.c.referral_count, 0)),
                        all_users.c.sender_id
                    ]
                ).label('rank')
            ).outerjoin(referral_count, all_users.c.sender_id == referral_count.c.sender_id).subquery()

            # Query to get the rank for the specific user
            query = db.query(ranking.c.rank, ranking.c.referral_count, ranking.c.user_id)
            query = query.filter(ranking.c.user_id == user_id)

            logging.info(f"Executing query: {query}")
            result = query.first()

            if result is None:
                logging.error(f"Ranking not found for user_id={user_id}")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ranking not found for the user")

            logging.info(f"Query result: {result}")

            response = {
                "rank": result.rank,
                "referral_count": result.referral_count,
                "user_id": result.user_id
            }

            logging.info(f"Returning response: {response}")

            return response
    
        except SQLAlchemyError as e:
            logging.error(f"Database error occurred: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error occurred: {str(e)}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


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
                has_claimed=friend_from_as_sender.has_claimed
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
                has_claimed=friend_from_as_receiver.has_claimed
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
                            status=friend.status,
                            has_claimed=friend.has_claimed
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
                            status=friend.status,
                            has_claimed=friend.has_claimed
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
                has_claimed=existing_friend.has_claimed,
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
                        has_claimed=f.has_claimed,
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
                has_claimed=db_friend.has_claimed,
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
                has_claimed=db_friend.has_claimed
            ),
            sender_id=db_friend.sender_id,
            receiver_id=db_friend.receiver_id,
        )
    )


def batch_update_by_user_id_to_receiver():
    pass

def batch_update_reward_claimed_by_sender_id(db: Session, sender_id: int) -> List[schemas.FriendDetailsResponseSchema]:
    """Update multiple friend has_claimed by list of sender id"""
    if sender_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing sender_id")
    try:
        existing_friends = db.query(FriendModel).filter(FriendModel.sender_id==sender_id).all()

        if not existing_friends:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friend not found")
        
        for friend in existing_friends:
            friend.has_claimed = True
            
        db.commit()
        
        return [
            schemas.FriendDetailsResponseSchema(
            friend_details=schemas.FriendDetailsSchema(
                friend_base=schemas.FriendSchema(
                    id=f.id,
                    status=f.status,
                    has_claimed=f.has_claimed,
                    created_at=f.created_at,
                    updated_at=f.updated_at,
                    custom_logs=f.custom_logs
                ),
                sender_id=f.sender_id,
                receiver_id=f.receiver_id,
            )
        )
            for f in existing_friends
        ]
    except Exception as e:
        logging.error(f"An error occured: {e}")


def remove_friend(sender_id: int, receiver_id: int, db: Session):
    friendship = get_Friend_by_sender_id_receiver_id(sender_id, db, receiver_id)
    if friendship:
        db.delete(friendship)
        db.commit()
    else:
        raise ValueError("Friendship not found")
