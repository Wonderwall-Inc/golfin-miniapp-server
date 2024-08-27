"""User App Business Logics"""

from operator import ge
from typing import Dict, Any
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session, joinedload, subqueryload
from app.user.models import UserModel
from app.user.schemas import (
    UserAppInfoSchema,
    UserPersonalInfoSchema,
    UserTelegramInfoSchema,
    UserCreateRequestSchema,
    UserCreateResponseSchema,
    UserRetrivalRequestSchema,
    UserRetrivalResponseSchema,
    UserUpdateRequestSchema,
    UserUpdateResponseSchema,
    UserUpdateDetailsSchema,
    UserDetailsSchema,
    UserSchema,
    UserDetailsResponseSchema,
)


class SchemaFactory:
    """Factory for creating schema objects"""

    def __init__(
        self,
        payload: (
            UserCreateRequestSchema
            | UserSchema
            | UserDetailsSchema
            | UserUpdateDetailsSchema
        ),
    ):
        self.payload = payload

    def userAppInfoSchemaMaker(self) -> UserAppInfoSchema:
        return UserAppInfoSchema(
            is_active=self.payload.app_info.is_active,
            in_game_items=self.payload.app_info.is_active,
            is_admin=self.payload.app_info.is_admin,
            skin=self.payload.app_info.skin,
        )

    def userPersonalInfoSchemaMaker(self) -> UserPersonalInfoSchema:
        return UserAppInfoSchema(
            location=self.payload.personal_info.location,
            nationality=self.payload.personal_info.nationality,
            age=self.payload.personal_info.age,
            gender=self.payload.personal_info.gender,
            email=self.payload.personal_info.email,
        )

    def userTelegramInfoSchemaMaker(self) -> UserTelegramInfoSchema:
        return UserTelegramInfoSchema(
            username=self.payload.telegram_info.username,
            telegram_id=self.payload.telegram_info.telegram_id,
            token_balance=self.payload.telegram_info.token_balance,
            is_premium=self.payload.telegram_info.is_premium,
            wallet_address=self.payload.telegram_info.wallet_address,
            chat_id=self.payload.telegram_info.chat_id,
        )

    def userSchemaMaker(self) -> UserSchema:
        return UserSchema(
            id=self.payload.id,
            app_info=self.userAppInfoSchemaMaker(),
            personal_info=self.userPersonalInfoSchemaMaker(),
            telegram_info=self.userTelegramInfoSchemaMaker(),
            created_at=self.payload.created_at,
            updated_at=self.payload.updated_at,
            custom_logs=self.payload.custom_logs,
        )

    def userCreateResponseSchemaMaker(self) -> UserCreateResponseSchema:
        return UserCreateResponseSchema(
            access_token=self.payload.access_token,
            user_details=UserDetailsSchema(user_base=self.userSchemaMaker()),
        )

    def userDetailsResponseSchemaMaker(self) -> UserDetailsResponseSchema:
        return UserDetailsSchema(
            user_base=self.userSchemaMaker(),
            game_characters=self.payload.game_characters,
            point=self.payload.point,
            activity=self.payload.activity,
            social_media=self.payload.social_media,
            sender=self.payload.sender,
            reciver=self.payload.receiver,
        )

    def userUpdateResponseSchemaMaker(self) -> UserUpdateResponseSchema:
        return UserUpdateResponseSchema(
            user_details=self.userDetailsResponseSchemaMaker()
        )

    # def userUpdateDetailsSchemaMaker(self) -> UserUpdateDetailsSchema:
    #     return UserUpdateDetailsSchema(
    #         token_balance=self.payload.token_balance,
    #         is_active=self.payload.is_active,
    #         is_premium=self.payload.is_premium,
    #         in_game_items=self.payload.in_game_items,
    #         skin=self.payload.skin,
    #         location=self.payload.location,
    #         age=self.payload.age,
    #         custom_logs=self.payload.custom_logs,
    #     )


def create_user(
    request: UserCreateRequestSchema, db: Session, background_tasks: BackgroundTasks
) -> UserCreateResponseSchema:
    """Create new user account"""
    if (
        not request.telegram_info.username
        or not request.telegram_info.telegram_id
        or not request.telegram_info.is_premium
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and Telegram id and is_premium are required",
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"User already exists"
        )
    schemaFactory = SchemaFactory(request)
    new_user = UserModel(
        access_token=request.access_token,
        app_info=schemaFactory.userAppInfoSchemaMaker(),
        personal_info=schemaFactory.userPersonalInfoSchemaMaker(),
        telegran_info=schemaFactory.userTelegramInfoSchemaMaker(),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create Game Character for the new user with bg task
    # Create Point for the new user with bg task
    # Create Point for the new user with bg task
    # Create Point for the new user with bg task
    # Create Point for the new user with bg task

    new_user_schemaFactory = SchemaFactory(new_user)
    return UserCreateResponseSchema(
        access_token=new_user.access_token,
        user_details=UserDetailsSchema(
            user_base=new_user_schemaFactory.userSchemaMaker()
        ),
    )


def retrival_user(
    request: UserRetrivalRequestSchema, db: Session
) -> UserRetrivalResponseSchema:
    base_query = db.query(UserModel)
    if request.id:
        base_query.filter(UserModel.id == request.id)
    if request.username:
        base_query.filter(UserModel.username == request.username)
    if request.telegram_id:
        base_query.filter(UserModel.telegram_id == request.telegram_id)
    if request.wallet_address:
        base_query.filter(UserModel.wallet_address == request.wallet_address)
    existing_user = base_query.options(
        joinedload(UserModel.point),  # Load point with the user
        joinedload(UserModel.game_characters),  # Load game character with the user
        joinedload(UserModel.activity),  # Load activity with the user
        joinedload(UserModel.social_media),  # Load social media with the user
        joinedload(UserModel.sender),  # Load sender with the user
        joinedload(UserModel.receiver),  # Load receiver with the user
    ).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {request} not found",
        )
    return UserRetrivalResponseSchema(
        user_details=SchemaFactory.userDetailsResponseSchemaMaker(existing_user)
    )


def retrival_users(skip: int, limit: int, db: Session):  # no filter
    existing_users = (
        db.query(UserModel)
        .options(
            joinedload(UserModel.point),  # Load point with the user
            joinedload(UserModel.game_characters),  # Load game character with the user
            joinedload(UserModel.activity),  # Load activity with the user
            joinedload(UserModel.social_media),  # Load social media with the user
            joinedload(UserModel.sender),  # Load sender with the user
            joinedload(UserModel.receiver),  # Load receiver with the user
        )
        .offset(skip)
        .limit(limit)
        .all()
    )
    return existing_users


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
    if request.user_payload:
        if request.user_payload.token_balance:
            existing_user.token_balance = request.user_payload.token_balance

        if request.user_payload.is_active:
            existing_user.is_active = request.user_payload.is_active

        if request.user_payload.is_premium:
            existing_user.is_premium = request.user_payload.is_premium

        if request.user_payload.in_game_items:
            existing_user.in_game_items = request.user_payload.in_game_items

        if request.user_payload.skin:
            existing_user.skin = request.user_payload.skin

        if request.user_payload.location:
            existing_user.location = request.user_payload.location

        if request.user_payload.age:
            existing_user.age = request.user_payload.age

        if request.user_payload.custom_logs:
            existing_user.custom_logs = request.user_payload.custom_logs
    db.commit()
    db.refresh(existing_user)
    return SchemaFactory.userUpdateResponseSchemaMaker(existing_user)


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
