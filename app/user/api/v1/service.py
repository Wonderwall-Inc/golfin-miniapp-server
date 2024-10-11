"""User App Business Logics"""

from fastapi import HTTPException, status, BackgroundTasks
import pytz
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.user.models import UserModel
from app.user.schemas import (
    UserAppInfoSchema,
    UserPersonalInfoSchema,
    UserTelegramInfoSchema,
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserRetrievalRequestSchema,
    UserRetrievalResponseSchema,
    UserUpdateRequestSchema,
    UserUpdateResponseSchema,
    UserUpdateDetailsSchema,
    UserDetailsSchema,
    UserSchema,
    UserDetailsResponseSchema,
    ReferralRankingResponse
)
from app.friend.schemas import FriendBaseSchema, FriendIds
from app.game_character.schemas import GameCharacterBaseSchema
from app.point.schemas import PointSchema
from app.social_media.schemas import SocialMediaBaseSchema
from app.activity.schemas import ActivityBaseSchema
# from core.utils import UserSchemaFactory
# from app.record.models import RecordModel
# from app.record.schemas import RecordSchema 
from app.record.api.v1.service import create_record, retrieve_record_by_user_id
from app.record.schemas import RecordCreateRequestSchema, RecordCreateDetailsSchema

def create_user(
    request: UserCreateRequestSchema, db: Session, 
    background_tasks: BackgroundTasks
):
    """Create new user account"""
    print(request)
    # if not request.telegram_info.username:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Username is required",
    #     )
    if not request.telegram_info.telegram_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Telegram Id is required",
        )
    if not request.personal_info.location or not request.personal_info.nationality:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location and Nationality are required",
        )
        
    user = (
        db.query(UserModel)
        .filter(UserModel.telegram_id == request.telegram_info.telegram_id)
        .first()
    )
    if user:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User existed"
        )
    user_app_info = UserAppInfoSchema(
        active=request.app_info.active,
        in_game_items=request.app_info.in_game_items,
        admin=request.app_info.admin,
        skin=request.app_info.skin,
        custom_logs=request.app_info.custom_logs,
    )
    user_personal_info = UserPersonalInfoSchema(
        location=request.personal_info.location,
        nationality=request.personal_info.nationality,
        age=request.personal_info.age,
        gender=request.personal_info.gender,
        email=request.personal_info.email,
    )
    user_telegram_info = UserTelegramInfoSchema(
        username=request.telegram_info.username,
        telegram_id=request.telegram_info.telegram_id,
        token_balance=request.telegram_info.token_balance,
        premium=request.telegram_info.premium,
        wallet_address=request.telegram_info.wallet_address,
        chat_id=request.telegram_info.chat_id,
        start_param=request.telegram_info.start_param,
    )
    new_user = UserModel(
        access_token=request.access_token,
        active=request.app_info.active,
        in_game_items=request.app_info.in_game_items,
        admin=request.app_info.admin,
        skin=request.app_info.skin,
        custom_logs=request.app_info.custom_logs,
        location=request.personal_info.location,
        nationality=request.personal_info.nationality,
        age=request.personal_info.age,
        gender=request.personal_info.gender,
        email=request.personal_info.email,
        username=request.telegram_info.username,
        telegram_id=request.telegram_info.telegram_id,
        token_balance=request.telegram_info.token_balance,
        premium=request.telegram_info.premium,
        wallet_address=request.telegram_info.wallet_address,
        chat_id=request.telegram_info.chat_id,
        start_param=request.telegram_info.start_param,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # FIXME
    record_req = RecordCreateRequestSchema(
        user_id = new_user.id,
        access_token='',
        record_details=RecordCreateDetailsSchema(
            action='CREATE',
            table='USER',
            table_id=new_user.id,
        )
    )
    background_tasks.add_task(create_record, record_req, db)
    # FIXME: Create Game Character for the new user with bg task
    # Create Point for the new user with bg task

    # new_user_schema_factory = UserSchemaFactory(new_user)
       
    return UserCreateResponseSchema(
        access_token=new_user.access_token,
        user_details=UserDetailsSchema(
            user_base=UserSchema(
                id=new_user.id,
                app_info=user_app_info,
                personal_info=user_personal_info,
                telegram_info=user_telegram_info,
                created_at=new_user.created_at.astimezone(pytz.timezone('Asia/Singapore')) if new_user.created_at else None, 
                updated_at=new_user.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if new_user.updated_at else None, 
                custom_logs=new_user.custom_logs,
            ),
        ),
    )

   
# def retrieve_user_by_id(id: int, db: Session):
#     if not id:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Missing User id",
#         )
#     existing_user = (
#         db.query(UserModel)
#         .filter(UserModel.id == id)
#         .options(
#             joinedload(UserModel.point),  # Load point with the user
#             joinedload(UserModel.game_characters),  # Load game character with the user
#             joinedload(UserModel.activity),  # Load activity with the user
#             joinedload(UserModel.social_media),  # Load social media with the user
#             joinedload(UserModel.sender),  # Load sender with the user
#             joinedload(UserModel.receiver),  # Load receiver with the user
#         )
#         .first()
#     )

#     if not existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with {id} not found",
#         )
#     user_app_info = UserAppInfoSchema(
#         active=existing_user.active,
#         in_game_items=existing_user.in_game_items,
#         admin=existing_user.admin,
#         skin=existing_user.skin,
#     )
#     user_personal_info = UserPersonalInfoSchema(
#         location=existing_user.location,
#         nationality=existing_user.nationality,
#         age=existing_user.age,
#         gender=existing_user.gender,
#         email=existing_user.email,
#     )
#     user_telegram_info = UserTelegramInfoSchema(
#         username=existing_user.username,
#         telegram_id=existing_user.telegram_id,
#         token_balance=existing_user.token_balance,
#         premium=existing_user.premium,
#         wallet_address=existing_user.wallet_address,
#         chat_id=existing_user.chat_id,
#     )
#     # return existing_user
#     user_base = UserSchema(
#         id=existing_user.id,
#         app_info=user_app_info,
#         personal_info=user_personal_info,
#         telegram_info=user_telegram_info,
#         created_at=existing_user.created_at,
#         updated_at=existing_user.updated_at,
#         custom_logs=existing_user.custom_logs,
#     )
#     sender_payload = [
#         FriendBaseSchema(
#             id=single_sender.id,
#             sender_id=single_sender.sender_id,
#             receiver_id=single_sender.receiver_id,
#             created_at=single_sender.created_at,
#             updated_at=single_sender.updated_at,
#             status=single_sender.status,
#         )
#         for single_sender in existing_user.sender
#     ]

#     receiver_payload = [
#         FriendBaseSchema(
#             id=single_receiver.id,
#             sender_id=single_receiver.sender_id,
#             receiver_id=single_receiver.receiver_id,
#             created_at=single_receiver.created_at,
#             updated_at=single_receiver.updated_at,
#             status=single_receiver.status,
#         )
#         for single_receiver in existing_user.receiver
#     ]

#     game_character_payload = [
#         GameCharacterBaseSchema(
#             id=single_game_character.id,
#             first_name=single_game_character.first_name,
#             last_name=single_game_character.last_name,
#             gender=single_game_character.gender,
#             title=single_game_character.title,
#             created_at=single_game_character.created_at,
#             updated_at=single_game_character.updated_at,
#             custom_logs=single_game_character.custom_logs,
#         )
#         for single_game_character in existing_user.game_characters
#     ]

#     point_payload = [
#         PointSchema(
#             id=p.id,
#             amount=p.amount,
#             extra_profit_per_hour=p.extra_profit_per_hour,
#             created_at=p.created_at,
#             updated_at=p.updated_at,
#             custom_logs=p.custom_logs,
#         )
#         for p in existing_user.point
#     ]

#     social_media_payload = [
#         SocialMediaBaseSchema(
#             id=so.id,
#             youtube_id=so.youtube_id,
#             youtube_following=so.youtube_following,
#             youtube_viewed=so.youtube_viewed,
#             youtube_view_date=so.youtube_view_date,
#             facebook_id=so.facebook_id,
#             facebook_following=so.facebook_following,
#             facebook_followed_date=so.facebook_followed_date,
#             instagram_id=so.instagram_id,
#             instagram_following=so.instagram_following,
#             instagram_follow_trigger_verify_date=so.instagram_follow_trigger_verify_date,
#             instagram_followed_date=so.instagram_followed_date,
#             instagram_tagged=so.instagram_tagged,
#             instagram_tagged_date=so.instagram_tagged_date,
#             instagram_reposted=so.instagram_reposted,
#             instagram_reposted_date=so.instagram_reposted_date,
#             telegram_id=so.telegram_id,
#             telegram_following=so.telegram_following,
#             telegram_followed_date=so.telegram_followed_date,
#             x_id=so.x_id,
#             x_following=so.x_following,
#             x_followed_date=so.x_followed_date,
#             discord_id=so.discord_id,
#             discord_following=so.discord_following,
#             discord_followed_date=so.discord_followed_date,
#             custom_logs=so.custom_logs,
#             updated_at=so.updated_at,
#             created_at=so.created_at,
#         )
#         for so in existing_user.social_media
#     ]

#     activity_payload = [
#         ActivityBaseSchema(
#             id=a.id,
#             logged_in=a.logged_in,
#             login_streak=a.login_streak,
#             total_logins=a.total_logins,
#             last_action_time=a.last_action_time,
#             last_login_time=a.last_login_time,
#             created_at=a.created_at,
#             updated_at=a.updated_at,
#             custom_logs=a.custom_logs,
#         )
#         for a in existing_user.activity
#     ]
#     user_details = UserDetailsSchema(
#         user_base=user_base,
#         game_characters=game_character_payload,
#         point=point_payload,
#         activity=activity_payload,
#         social_media=social_media_payload,
#         receiver=receiver_payload,
#         sender=sender_payload,
#     )
#     return UserRetrievalResponseSchema(user_details=user_details)


def retrieve_user(
    id: Optional[int],
    username: Optional[str],
    telegram_id: Optional[str],
    wallet_address: Optional[str],
    db: Session,
    # background_tasks: BackgroundTasks
):
    if not id and not username and not telegram_id and not wallet_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required parameter",
        )

    base_query = db.query(UserModel)
    filters = []  # inclusive AND case
    if id is not None:
        filters.append(UserModel.id == id)
    if username is not None:
        filters.append(UserModel.username == username)
    if telegram_id is not None:
        filters.append(UserModel.telegram_id == telegram_id)
    if wallet_address is not None:
        filters.append(UserModel.wallet_address == wallet_address)

    if filters:
        existing_user = base_query.filter(*filters).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} not found",
        )

    user_app_info = UserAppInfoSchema(
        active=existing_user.active,
        in_game_items=existing_user.in_game_items,
        admin=existing_user.admin,
        skin=existing_user.skin,
    )

    user_personal_info = UserPersonalInfoSchema(
        location=existing_user.location,
        nationality=existing_user.nationality,
        age=existing_user.age,
        gender=existing_user.gender,
        email=existing_user.email,
    )

    user_telegram_info = UserTelegramInfoSchema(
        username=existing_user.username,
        telegram_id=existing_user.telegram_id,
        token_balance=existing_user.token_balance,
        premium=existing_user.premium,
        wallet_address=existing_user.wallet_address,
        chat_id=existing_user.chat_id,
        start_param=existing_user.start_param
    )


    return UserDetailsResponseSchema(
        user_details=UserDetailsSchema(
            user_base=UserSchema(
                id=existing_user.id,
                app_info=user_app_info,
                personal_info=user_personal_info,
                telegram_info=user_telegram_info,
                created_at=existing_user.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.created_at else None, 
                updated_at=existing_user.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.updated_at else None, 
                custom_logs=existing_user.custom_logs,
            )
        )
    )

def retrieve_user_extra_detail(
    id: Optional[int],
    username: Optional[str],
    telegram_id: Optional[str],
    wallet_address: Optional[str],
    db: Session,
    # background_tasks: BackgroundTasks
):
    if not id and not username and not telegram_id and not wallet_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required parameter",
        )

    base_query = db.query(UserModel)
    filters = []  # inclusive AND case
    if id is not None:
        filters.append(UserModel.id == id)
    if username is not None:
        filters.append(UserModel.username == username)
    if telegram_id is not None:
        filters.append(UserModel.telegram_id == telegram_id)
    if wallet_address is not None:
        filters.append(UserModel.wallet_address == wallet_address)

    if filters:
        base_query = base_query.filter(*filters)
        existing_user = base_query.options(
            joinedload(UserModel.point),  # Load point with the user
            joinedload(UserModel.game_characters),  # Load game character with the user
            joinedload(UserModel.activity),  # Load activity with the user
            joinedload(UserModel.social_media),  # Load social media with the user
            joinedload(UserModel.sender),  # Load sender with the user
            joinedload(UserModel.receiver),  # Load receiver with the user
            # joinedload(UserModel.record)     # FIXME:
        ).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} not found",
        )

    user_app_info = UserAppInfoSchema(
        active=existing_user.active,
        in_game_items=existing_user.in_game_items,
        admin=existing_user.admin,
        skin=existing_user.skin,
    )

    user_personal_info = UserPersonalInfoSchema(
        location=existing_user.location,
        nationality=existing_user.nationality,
        age=existing_user.age,
        gender=existing_user.gender,
        email=existing_user.email,
    )

    user_telegram_info = UserTelegramInfoSchema(
        username=existing_user.username,
        telegram_id=existing_user.telegram_id,
        token_balance=existing_user.token_balance,
        premium=existing_user.premium,
        wallet_address=existing_user.wallet_address,
        chat_id=existing_user.chat_id,
        start_param=existing_user.start_param
    )

    sender_payload = [
        FriendBaseSchema(
            id=single_sender.id,
            sender_id=single_sender.sender_id,
            receiver_id=single_sender.receiver_id,
            created_at=single_sender.created_at,
            updated_at=single_sender.updated_at,
            status=single_sender.status,
            has_claimed=single_sender.has_claimed
        )
        for single_sender in existing_user.sender
    ]

    receiver_payload = [
        FriendBaseSchema(
            id=single_receiver.id,
            sender_id=single_receiver.sender_id,
            receiver_id=single_receiver.receiver_id,
            created_at=single_receiver.created_at,
            updated_at=single_receiver.updated_at,
            status=single_receiver.status,
            has_claimed=single_receiver.has_claimed
        )
        for single_receiver in existing_user.receiver
    ]

    point_payload = [
        PointSchema(
            id=p.id,
            login_amount=p.login_amount,
            referral_amount=p.referral_amount,
            extra_profit_per_hour=p.extra_profit_per_hour,
            created_at=p.created_at,
            updated_at=p.updated_at,
            custom_logs=p.custom_logs,
        )
        for p in existing_user.point
    ]

    social_media_payload = [
        SocialMediaBaseSchema(
            id=so.id,
            youtube_id=so.youtube_id,
            youtube_following=so.youtube_following,
            youtube_viewed=so.youtube_viewed,
            youtube_view_date=so.youtube_view_date,
            facebook_id=so.facebook_id,
            facebook_following=so.facebook_following,
            facebook_followed_date=so.facebook_followed_date,
            instagram_id=so.instagram_id,
            instagram_following=so.instagram_following,
            instagram_follow_trigger_verify_date=so.instagram_follow_trigger_verify_date,
            instagram_followed_date=so.instagram_followed_date,
            instagram_tagged=so.instagram_tagged,
            instagram_tagged_date=so.instagram_tagged_date,
            instagram_reposted=so.instagram_reposted,
            instagram_reposted_date=so.instagram_reposted_date,
            telegram_id=so.telegram_id,
            telegram_following=so.telegram_following,
            telegram_followed_date=so.telegram_followed_date,
            x_id=so.x_id,
            x_following=so.x_following,
            x_followed_date=so.x_followed_date,
            discord_id=so.discord_id,
            discord_following=so.discord_following,
            discord_followed_date=so.discord_followed_date,
            custom_logs=so.custom_logs,
            updated_at=so.updated_at,
            created_at=so.created_at,
        )
        for so in existing_user.social_media
    ]

    activity_payload = [
        ActivityBaseSchema(
            id=a.id,
            logged_in=a.logged_in,
            login_streak=a.login_streak,
            total_logins=a.total_logins,
            last_action_time=a.last_action_time,
            last_login_time=a.last_login_time,
            created_at=a.created_at,
            updated_at=a.updated_at,
            custom_logs=a.custom_logs,
        )
        for a in existing_user.activity
    ]
    
    # FIXME
    # new_record = background_tasks.add_task(retrieve_record_by_user_id, existing_user.id, db)
    # print('new_record')
    # print(new_record)
    # existing_user.record.append(new_record)
    
    # record_payload = [
    #     RecordSchema(
    #         id=r.id,
    #         action=r.action,
    #         table=r.table,
    #         table_id=r.table_id,
    #         created_at=r.created_at,
    #         updated_at=r.updated_at,
    #         custom_logs=r.custom_logs,
    #     )
    #     for r in new_record
    # ]

    return UserDetailsResponseSchema(
        user_details=UserDetailsSchema(
            user_base=UserSchema(
                id=existing_user.id,
                app_info=user_app_info,
                personal_info=user_personal_info,
                telegram_info=user_telegram_info,
                created_at=existing_user.created_at,
                updated_at=existing_user.updated_at,
                custom_logs=existing_user.custom_logs,
            ),
            game_characters=[
                GameCharacterBaseSchema(
                    id=single_game_character.id,
                    first_name=single_game_character.first_name,
                    last_name=single_game_character.last_name,
                    gender=single_game_character.gender,
                    title=single_game_character.title,
                    created_at=single_game_character.created_at,
                    updated_at=single_game_character.updated_at,
                    custom_logs=single_game_character.custom_logs,
                )
                for single_game_character in existing_user.game_characters
            ],
            point=point_payload,
            activity=activity_payload,
            social_media=social_media_payload,
            # record=new_record, # FIXME
            sender=sender_payload,
            receiver=receiver_payload,
        )
    )


def retrieve_users(
    db: Session, skip: int, limit: int
) -> List[UserDetailsResponseSchema]:  # no filter
    existing_users = (
        db.query(UserModel)
        .options(
            joinedload(UserModel.point),  # Load point with the user
            joinedload(UserModel.game_characters),  # Load game character with the user
            joinedload(UserModel.activity),  # Load activity with the user
            joinedload(UserModel.social_media),  # Load social media with the user
            joinedload(UserModel.sender),  # Load sender with the user
            joinedload(UserModel.receiver),  # Load receiver with the user
            # joinedload(UserModel.record) # FIXME
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    # FIXME
    # for existing_user in existing_users:
    #     new_record = RecordModel(action="LIST", table="USER",table_id=existing_user.id)
    #     db.add(new_record)
    #     db.commit()
    #     db.refresh(new_record)
    
    return [
        UserDetailsResponseSchema(
            user_details=UserDetailsSchema(
                user_base=UserSchema(
                    id=existing_user.id,
                    app_info=UserAppInfoSchema(
                        active=existing_user.active,
                        in_game_items=existing_user.in_game_items,
                        admin=existing_user.admin,
                        skin=existing_user.skin,
                    ),
                    personal_info=UserPersonalInfoSchema(
                        location=existing_user.location,
                        nationality=existing_user.nationality,
                        age=existing_user.age,
                        gender=existing_user.gender,
                        email=existing_user.email,
                    ),
                    telegram_info=UserTelegramInfoSchema(
                        username=existing_user.username,
                        telegram_id=existing_user.telegram_id,
                        token_balance=existing_user.token_balance,
                        premium=existing_user.premium,
                        wallet_address=existing_user.wallet_address,
                        chat_id=existing_user.chat_id,
                        start_param=existing_user.start_param
                    ),
                    created_at=existing_user.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.created_at else None, 
                    updated_at=existing_user.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.updated_at else None, 
                    custom_logs=existing_user.custom_logs,
                ),
                game_characters=[
                    GameCharacterBaseSchema(
                        id=single_game_character.id,
                        first_name=single_game_character.first_name,
                        last_name=single_game_character.last_name,
                        gender=single_game_character.gender,
                        title=single_game_character.title,
                        created_at=single_game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_game_character.created_at else None, 
                        updated_at=single_game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_game_character.updated_at else None, 
                        custom_logs=single_game_character.custom_logs,
                    )
                    for single_game_character in existing_user.game_characters
                ],
                point=[
                    PointSchema(
                        id=p.id,
                        login_amount=p.login_amount,
                        referral_amount=p.referral_amount,
                        extra_profit_per_hour=p.extra_profit_per_hour,
                        created_at=p.created_at.astimezone(pytz.timezone('Asia/Singapore')) if p.created_at else None, 
                        updated_at=p.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if p.updated_at else None, 
                        custom_logs=p.custom_logs,
                    )
                    for p in existing_user.point
                ],
                activity=[
                    ActivityBaseSchema(
                        id=a.id,
                        logged_in=a.logged_in,
                        login_streak=a.login_streak,
                        total_logins=a.total_logins,
                        last_action_time=a.last_action_time.astimezone(pytz.timezone('Asia/Singapore')) if a.last_action_time else None, 
                        last_login_time=a.last_login_time.astimezone(pytz.timezone('Asia/Singapore')) if a.last_login_time else None, 
                        created_at=a.created_at.astimezone(pytz.timezone('Asia/Singapore')) if a.created_at else None, 
                        updated_at=a.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if a.updated_at else None, 
                        custom_logs=a.custom_logs,
                    )
                    for a in existing_user.activity
                ],
                social_media=[
                    SocialMediaBaseSchema(
                        id=so.id,
                        youtube_id=so.youtube_id,
                        youtube_following=so.youtube_following,
                        youtube_viewed=so.youtube_viewed,
                        youtube_view_date=so.youtube_view_date.astimezone(pytz.timezone('Asia/Singapore')) if so.youtube_view_date else None, 
                        facebook_id=so.facebook_id,
                        facebook_following=so.facebook_following,
                        facebook_followed_date=so.facebook_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.facebook_followed_date else None, 
                        instagram_id=so.instagram_id,
                        instagram_following=so.instagram_following,
                        instagram_follow_trigger_verify_date=so.instagram_follow_trigger_verify_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_follow_trigger_verify_date else None, 
                        instagram_followed_date=so.instagram_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_followed_date else None, 
                        instagram_tagged=so.instagram_tagged,
                        instagram_tagged_date=so.instagram_tagged_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_tagged_date else None, 
                        instagram_reposted=so.instagram_reposted,
                        instagram_reposted_date=so.instagram_reposted_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_reposted_date else None, 
                        telegram_id=so.telegram_id,
                        telegram_following=so.telegram_following,
                        telegram_followed_date=so.telegram_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.telegram_followed_date else None, 
                        x_id=so.x_id,
                        x_following=so.x_following,
                        x_followed_date=so.x_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.x_followed_date else None, 
                        discord_id=so.discord_id,
                        discord_following=so.discord_following,
                        discord_followed_date=so.discord_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.discord_followed_date else None, 
                        custom_logs=so.custom_logs,
                        updated_at=so.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if so.updated_at else None, 
                        created_at=so.created_at.astimezone(pytz.timezone('Asia/Singapore')) if so.created_at else None,
                    )
                    for so in existing_user.social_media
                ],
                sender=[
                    FriendBaseSchema(
                        id=single_sender.id,
                        sender_id=single_sender.sender_id,
                        receiver_id=single_sender.receiver_id,
                        created_at=single_sender.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_sender.created_at else None,
                        updated_at=single_sender.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_sender.updated_at else None,
                        status=single_sender.status,
                        has_claimed=single_sender.has_claimed
                    )
                    for single_sender in existing_user.sender
                ],
                receiver=[
                    FriendBaseSchema(
                        id=single_receiver.id,
                        sender_id=single_receiver.sender_id,
                        receiver_id=single_receiver.receiver_id,
                        created_at=single_receiver.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_receiver.created_at else None,
                        updated_at=single_receiver.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_receiver.updated_at else None,
                        status=single_receiver.status,
                        has_claimed=single_receiver.has_claimed
                    )
                    for single_receiver in existing_user.receiver
                ],
                # FIXME
                # record_payload = [
                #     RecordSchema(
                #         id=r.id,
                #         action=r.action,
                #         table=r.table,
                #         table_id=r.table_id,
                #         created_at=r.created_at,
                #         updated_at=r.updated_at,
                #         custom_logs=r.custom_logs,
                #     )
                #     for r in existing_user.record
                # ]

            )
        )
        for existing_user in existing_users
    ]


def update_user(
    request: UserUpdateRequestSchema, db: Session
) -> UserUpdateResponseSchema:
    if not request.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing paramters"
        )
    existing_user = db.query(UserModel).filter(UserModel.id == request.id).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found"
        )
    if existing_user:
        if request.user_payload:
            if request.user_payload.token_balance:
                existing_user.token_balance = request.user_payload.token_balance

            if request.user_payload.active:
                existing_user.active = request.user_payload.active

            if request.user_payload.premium:
                existing_user.premium = request.user_payload.premium

            if request.user_payload.in_game_items:
                existing_user.in_game_items = request.user_payload.in_game_items

            if request.user_payload.skin:
                existing_user.skin = request.user_payload.skin

            if request.user_payload.location:
                existing_user.location = request.user_payload.location

            if request.user_payload.age:
                existing_user.age = request.user_payload.age
           
            if request.user_payload.username:
                existing_user.username = request.user_payload.username

            if request.user_payload.custom_logs:
                existing_user.custom_logs = request.user_payload.custom_logs
            
            db.commit()
            db.refresh(existing_user)

            user_app_info = UserAppInfoSchema(
                active=existing_user.active,
                in_game_items=existing_user.in_game_items,
                admin=existing_user.admin,
                skin=existing_user.skin,
            )

            user_personal_info = UserPersonalInfoSchema(
                location=existing_user.location,
                nationality=existing_user.nationality,
                age=existing_user.age,
                gender=existing_user.gender,
                email=existing_user.email,
            )

            user_telegram_info = UserTelegramInfoSchema(
                username=existing_user.username,
                telegram_id=existing_user.telegram_id,
                token_balance=existing_user.token_balance,
                premium=existing_user.premium,
                wallet_address=existing_user.wallet_address,
                chat_id=existing_user.chat_id,
                start_param=existing_user.start_param
            )

            sender_payload = [
                FriendBaseSchema(
                    id=single_sender.id,
                    sender_id=single_sender.sender_id,
                    receiver_id=single_sender.receiver_id,
                    created_at=single_sender.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_sender.created_at else None,
                    updated_at=single_sender.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_sender.updated_at else None,
                    status=single_sender.status,
                    has_claimed=single_sender.has_claimed
                )
                for single_sender in existing_user.sender
            ]

            receiver_payload = [
                FriendBaseSchema(
                    id=single_receiver.id,
                    sender_id=single_receiver.sender_id,
                    receiver_id=single_receiver.receiver_id,
                    created_at=single_receiver.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_receiver.created_at else None,
                    updated_at=single_receiver.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_receiver.updated_at else None,
                    status=single_receiver.status,
                    has_claimed=single_receiver.has_claimed
                )
                for single_receiver in existing_user.receiver
            ]

            game_character_payload = [
                GameCharacterBaseSchema(
                    id=single_game_character.id,
                    first_name=single_game_character.first_name,
                    last_name=single_game_character.last_name,
                    gender=single_game_character.gender,
                    title=single_game_character.title,
                    created_at=single_game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if single_game_character.created_at else None,
                    updated_at=single_game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if single_game_character.updated_at else None,
                    custom_logs=single_game_character.custom_logs,
                )
                for single_game_character in existing_user.game_characters
            ]

            point_payload = [
                PointSchema(
                    id=p.id,
                    login_amount=p.login_amount,
                    referral_amount=p.referral_amount,
                    extra_profit_per_hour=p.extra_profit_per_hour,
                    created_at=p.created_at.astimezone(pytz.timezone('Asia/Singapore')) if p.created_at else None,
                    updated_at=p.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if p.updated_at else None,
                    custom_logs=p.custom_logs,
                )
                for p in existing_user.point
            ]

            social_media_payload = [
                SocialMediaBaseSchema(
                    id=so.id,
                    youtube_id=so.youtube_id,
                    youtube_following=so.youtube_following,
                    youtube_viewed=so.youtube_viewed,
                    youtube_view_date=so.youtube_view_date.astimezone(pytz.timezone('Asia/Singapore')) if so.youtube_view_date else None,
                    facebook_id=so.facebook_id,
                    facebook_following=so.facebook_following,
                    facebook_followed_date=so.facebook_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.facebook_followed_date else None,
                    instagram_id=so.instagram_id,
                    instagram_following=so.instagram_following,
                    instagram_follow_trigger_verify_date=so.instagram_follow_trigger_verify_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_follow_trigger_verify_date else None,
                    instagram_followed_date=so.instagram_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_followed_date else None,
                    instagram_tagged=so.instagram_tagged,
                    instagram_tagged_date=so.instagram_tagged_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_tagged_date else None,
                    instagram_reposted=so.instagram_reposted,
                    instagram_reposted_date=so.instagram_reposted_date.astimezone(pytz.timezone('Asia/Singapore')) if so.instagram_reposted_date else None,
                    telegram_id=so.telegram_id,
                    telegram_following=so.telegram_following,
                    telegram_followed_date=so.telegram_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.telegram_followed_date else None,
                    x_id=so.x_id,
                    x_following=so.x_following,
                    x_followed_date=so.x_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.x_followed_date else None,
                    discord_id=so.discord_id,
                    discord_following=so.discord_following,
                    discord_followed_date=so.discord_followed_date.astimezone(pytz.timezone('Asia/Singapore')) if so.discord_followed_date else None,
                    custom_logs=so.custom_logs,
                    created_at=so.created_at.astimezone(pytz.timezone('Asia/Singapore')) if so.created_at else None,
                    updated_at=so.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if so.updated_at else None,
                )
                for so in existing_user.social_media
            ]

            activity_payload = [
                ActivityBaseSchema(
                    id=a.id,
                    logged_in=a.logged_in,
                    login_streak=a.login_streak,
                    total_logins=a.total_logins,
                    last_action_time=a.last_action_time.astimezone(pytz.timezone('Asia/Singapore')) if a.last_action_time else None,
                    last_login_time=a.last_login_time.astimezone(pytz.timezone('Asia/Singapore')) if a.last_login_time else None,
                    created_at=a.created_at.astimezone(pytz.timezone('Asia/Singapore')) if a.created_at else None,
                    updated_at=a.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if a.updated_at else None,
                    custom_logs=a.custom_logs,
                )
                for a in existing_user.activity
            ]

        return UserUpdateResponseSchema(
            user_details=UserDetailsSchema(
                user_base=UserSchema(
                    id=existing_user.id,
                    app_info=user_app_info,
                    personal_info=user_personal_info,
                    telegram_info=user_telegram_info,
                    created_at=existing_user.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.created_at else None,
                    updated_at=existing_user.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_user.updated_at else None,
                    custom_logs=existing_user.custom_logs,
                ),
                game_characters=game_character_payload,
                point=point_payload,
                activity=activity_payload,
                social_media=social_media_payload,
                sender=sender_payload,
                receiver=receiver_payload,
            )
        )


def delete_user(id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found"
        )


# Get users by ids
# TODO: add later
# def batch_get_user(user_ids: list[int], db: Session) -> list[User]:
#     result = []
#     for user_id in user_ids:
#         result.append(
#             sum[
#                 db.query(User)
#                 .filter(User.user_id == user_id)
#                 .options(
#                     joinedload(User.coins),  # Load coins with the user
#                     joinedload(User.sender),  # Load friends with the user
#                     joinedload(User.receiver),
#                 )
#                 .all(),
#                 [],
#             ]
#         )
#     return result

def get_referral_ranking(sender_id: int, db: Session) -> ReferralRankingResponse:  # no filter
    """Get referral ranking"""
    existing_users = (
        db.query(UserModel)
        .options(
            joinedload(UserModel.sender),  # Load sender with the user
            joinedload(UserModel.receiver),  # Load receiver with the user
        )
        .all()
    )
    
    # FIXME
    # for existing_user in existing_users:
    #     new_record = RecordModel(action="LIST", table="USER",table_id=existing_user.id)
    #     db.add(new_record)
    #     db.commit()
    #     db.refresh(new_record)
    
    user_referrals = [(user.id, len(user.sender)) for user in existing_users]
    
    # Sort the list by sender_list_length in descending order
    sorted_referrals = sorted(user_referrals, key=lambda x: x[1], reverse=True)
    
    # Get the top 10 users
    top_10 = sorted_referrals[:10]
    
    # Create the ranking list with rank, sender list length, user_id, and username
    ranking_list = []
    for rank, (user_id, sender_count) in enumerate(top_10, start=1):
        user = next(user for user in existing_users if user.id == user_id)
        ranking_list.append({
            "rank": rank,
            "sender_count": sender_count,
            "user_id": user_id,
            "telegram_id": user.telegram_id,
            "username": user.username
        })
    
    # Find the rank of the given sender_id
    sender_rank = next((rank for rank, (user_id, _) in enumerate(sorted_referrals, start=1) if user_id == sender_id), None)
    
    # Get the sender's record
    sender_record = next((user for user in existing_users if user.id == sender_id), None)
    sender_info = None
    if sender_record:
        sender_info = {
            "rank": sender_rank,
            "sender_count": len(sender_record.sender),
            "user_id": sender_id,
            "telegram_id": sender_record.telegram_id,
            "username": sender_record.username
        }
    
    # Determine if the sender is in the top 10
    sender_in_top_10 = any(record["user_id"] == sender_id for record in ranking_list)
    
    return {
        "top_10": ranking_list,
        "sender_info": sender_info,
        "sender_in_top_10": sender_in_top_10
    }