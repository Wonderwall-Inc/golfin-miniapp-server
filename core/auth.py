# """This module contains the authentication logic for the application."""

# from cachetools import TTLCache, cached
# from fastapi import Depends, HTTPException
# import httpx
# from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
# from sqlalchemy.orm import Session
# from app.user.models import UserModel
# from app.user.schemas import (
#     UserSchema,
#     UserAppInfoSchema,
#     UserPersonalInfoSchema,
#     UserTelegramInfoSchema,
# )
# from core import database
# from core.jwt_bearer import JWTBearer
# from core.models import JWTAuthorizationCredentials

# auth = JWTBearer()
# get_db = database.get_db


# async def get_current_user(
#     credentials: JWTAuthorizationCredentials = Depends(auth),
#     db: Session = Depends(get_db),
# ):
#     """
#     Retrieves the current user based on the provided JWT token.
#     Args:
#         credentials (JWTAuthorizationCredentials): The JWT authorization credentials.
#         db (Session): The database session.

#     Returns: UserInfoSchema: The user information.

#     Raises: HTTPException: If the token is invalid or the user is not found.
#     """

#     if credentials:
#         jwt_token = credentials.jwt_token

#         # Check if the user access token is already in the database
#         user = db.query(UserModel).filter(UserModel.access_token == jwt_token).first()

#         if not user:
#             # headers = {"Authorization": f"Bearer {jwt_token}"}
#             # async with httpx.AsyncClient() as client:
#             # response = await client.get(
#             #     info_url,
#             #     headers=headers,
#             # )
#             # if response.status_code != 200:
#             #     raise HTTPException(
#             #         status_code=HTTP_401_UNAUTHORIZED,
#             #         detail="Invalid token",
#             #         headers={"WWW-Authenticate": "Bearer"},
#             #     )

#             telegram_id = credentials.claims["telegram_id"]
#             if telegram_id:
#                 user = (
#                     db.query(UserModel)
#                     .filter(UserModel.telegram_id == telegram_id)
#                     .first()
#                 )

#             if not user:
#                 raise HTTPException(
#                     status_code=HTTP_404_NOT_FOUND,
#                     detail="User not found",
#                 )

#             user.access_token = jwt_token
#             db.commit()
#             db.refresh(user)

#         user_info = UserSchema(
#             id=user.id,
#             app_info=UserAppInfoSchema(
#                 is_active=user.is_active,
#                 in_game_items=user.in_game_items,
#                 is_admin=user.is_admin,
#                 skin=user.skin,
#                 custom_logs=user.custom_logs,
#             ),
#             personal_info=UserPersonalInfoSchema(
#                 location=user.location,
#                 nationality=user.nationality,
#                 age=user.age,
#                 gender=user.gender,
#                 email=user.email,
#             ),
#             telegram_info=UserTelegramInfoSchema(
#                 username=user.username,
#                 telegram_id=user.telegram_id,
#                 token_balance=user.token_balance,
#                 is_premium=user.is_premium,
#                 wallet_address=user.wallet_address,
#                 chat_id=user.chat_id,
#             ),
#             created_at=user.created_at,
#             updated_at=user.updated_at,
#             custom_logs=user.custom_logs,
#         )
#         return user_info
