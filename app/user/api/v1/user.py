"""User App API Routes"""

from typing import List, Optional
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from core import database
from app.user import schemas
from app.user.api.v1 import service

# from core.auth import auth, get_current_user


router = APIRouter(prefix="/api/v1/user", tags=["user"])
get_db = database.get_db


@router.post(
    "/create",
    response_model=schemas.UserCreateResponseSchema,
    # dependencies=[Depends(auth)],
)
def create_user(
    request: schemas.UserCreateRequestSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Login with existing account"""
    return service.create_user(request, db, background_tasks)


@router.get("/detail/{id}")
def get_detail_by_user_id(
    id: int,
    db: Session = Depends(get_db),
):
    """Get User details of single user by id"""
    return service.retrieve_user_by_id(id, db)


@router.get("/detail/")
def get_detail_user(
    id: int | None = None,
    username: str | None = None,
    telegram_id: str | None = None,
    wallet_address: str | None = None,
    db: Session = Depends(get_db),
):
    """Get User details of single user"""
    print("hello")
    return service.retrieve_user(id, username, telegram_id, wallet_address, db)


@router.get(
    "/details",
    response_model=List[schemas.UserDetailsResponseSchema],
    # dependencies=[Depends(auth)],
)
def get_detail_users(
    # user: schemas.UserSchema,
    skip: int = 0,
    limit: int = 15,
    # user: schemas.UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get Users if it is admin"""
    # if not user.app_info.is_admin:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="Not an admin"
    #     )

    return service.retrieve_users(db, skip, limit)


@router.put(
    "/update",
    response_model=schemas.UserUpdateResponseSchema,
    # dependencies=[Depends(auth)],
)
def update_user(
    request: schemas.UserUpdateRequestSchema, db: Session = Depends(get_db)
):
    """Update user details"""
    return service.update_user(request, db)
