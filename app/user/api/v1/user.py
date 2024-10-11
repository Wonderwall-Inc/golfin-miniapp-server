"""User App API Routes"""
import asyncio
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


@router.post("/create", response_model=schemas.UserCreateResponseSchema)# dependencies=[Depends(auth)],
# def create_user(request: schemas.UserCreateRequestSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db),):
async def create_user(request: schemas.UserCreateRequestSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Login with existing account"""
    return service.create_user(request, db, background_tasks)


# @router.get("/detail/{id}")
# def get_detail_by_user_id(
#     id: int,
#     db: Session = Depends(get_db),
# ):
#     """Get User details of single user by id"""
#     return service.retrieve_user_by_id(id, db)


    # background_tasks: BackgroundTasks, # FIXME
@router.get("/detail")
def get_user(id: Optional[int] = None, username: Optional[str] = None, telegram_id: Optional[str] = None, wallet_address: Optional[str] = None, db: Session = Depends(get_db)):
    """Get User details of single user"""
    return service.retrieve_user(id, username, telegram_id, wallet_address, db)

@router.get("/extra-detail")
def get_user_extra_detail(id: Optional[int] = None, username: Optional[str] = None, telegram_id: Optional[str] = None, wallet_address: Optional[str] = None, db: Session = Depends(get_db)):
    """Get User details of single user including information from other tables"""
    return service.retrieve_user_extra_detail(id, username, telegram_id, wallet_address, db)


@router.get("/details", response_model=List[schemas.UserDetailsResponseSchema])# dependencies=[Depends(auth)],
def get_user_list(
    # user: schemas.UserSchema,
    skip: int = 0,
    limit: int = 15,
    # user: schemas.UserSchema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get Users if it is admin"""
    return service.retrieve_users(db, skip, limit)


@router.put("/update", response_model=schemas.UserUpdateResponseSchema)# dependencies=[Depends(auth)],
def update_user(request: schemas.UserUpdateRequestSchema, db: Session = Depends(get_db)):
    """Update user details"""
    return service.update_user(request, db)


@router.get("/referral-ranking", response_model=schemas.ReferralRankingResponse)
def get_referral_ranking(sender_id: int, db: Session = Depends(get_db)):
    """Get referral ranking"""
    return service.get_referral_ranking(sender_id, db)

