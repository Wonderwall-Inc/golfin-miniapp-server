"""User App API Routes"""

from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from core import database

from app.game_character import schemas
from app.game_character.api.v1 import service


router = APIRouter(prefix="/api/v1/game_character", tags=["game_character"])
get_db = database.get_db


@router.post("/create", response_model=schemas.GameCharacterCreateResponseSchema)
def create_game_character(
    request: schemas.GameCharacterCreateRequestSchema, db: Session = Depends(get_db)
):
    """create character"""
    return service.create_game_character(request, db)


@router.get(
    "/detail/{game_character_id}",
    # response_model=schemas.GameCharacterRetrievalResponseSchema,
)
def get_detail_by_character_id(game_character_id: int, db: Session = Depends(get_db)):
    """get detail by id"""
    result = service.retrieve_game_character(game_character_id, db)
    return result


@router.get(
    "/detail/stat/{game_character_id}",
    response_model=schemas.GameCharacterStatRetrievalResponseSchema,
)
def get_stat_detail_by_id(game_character_id: int, db: Session = Depends(get_db)):
    """get stats detail by id"""
    return service.retrieve_game_character_stat(game_character_id, db)


@router.get("/detail/list/{user_id}", response_model=List[schemas.GameCharacterSchema])
def get_details(
    user_id: int, skip: int = 0, limit: int = 15, db: Session = Depends(get_db)
):
    """get details"""
    return service.retrieve_game_character_list(db, user_id, skip, limit)


@router.put("/update", response_model=schemas.GameCharacterUpdateResponseSchema)
def update_character(
    request: schemas.GameCharacterUpdateRequestSchema, db: Session = Depends(get_db)
):
    """update"""
    return service.update_game_character(request, db)
