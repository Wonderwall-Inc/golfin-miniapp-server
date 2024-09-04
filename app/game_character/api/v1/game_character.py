"""User App API Routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core import database
from app.game_character import schemas
from app.game_character.api.v1 import service


get_db = database.get_db

router = APIRouter(prefix="/api/v1/game_character", tags=["game_character"])


@router.post("/create", response_model=schemas.GameCharacterCreateResponseSchema)
def create_game_character(request: schemas.GameCharacterCreateRequestSchema, db: Session = Depends(get_db)):
    """Create New Game Character"""
    return service.create_game_character(request, db)


@router.get("/detail", response_model=List[schemas.GameCharacterRetrievalResponseSchema])
def get_game_character(game_character_id: Optional[int] = None, user_id: Optional[int] = None,db: Session = Depends(get_db)):
    """Retrieve Game Character Details from Single User"""
    return service.retrieve_game_character(game_character_id, user_id, db)


@router.get("/detail/stat",response_model=schemas.GameCharacterStatRetrievalResponseSchema | None)
def get_game_character_stat(id: Optional[int] = None, game_character_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Retrieve Game Character Stats from Single Character"""
    return service.retrieve_game_character_stat(id, game_character_id, db)

@router.get("/details/all/list", response_model=List[schemas.GameCharacterRetrievalResponseSchema])
def get_game_character_list(user_ids: List[int] = Query(default=None), skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve Game Character List from all Users"""
    return service.retrieve_game_character_all_list(db, user_ids, skip, limit)

@router.get("/detail/list/{user_id}", response_model=List[schemas.GameCharacterSchema])
def get_game_character_from_one_user(user_id: int, skip: int = 0, limit: int = 15, db: Session = Depends(get_db)):
    """Retrieve all Game Characters from Single User"""
    return service.retrieve_game_character_list_from_one_user(db, user_id, skip, limit)


@router.put("/update", response_model=schemas.GameCharacterUpdateResponseSchema)
def update_character(request: schemas.GameCharacterUpdateRequestSchema, db: Session = Depends(get_db)):
    """Update a Game Character with Stats"""
    return service.update_game_character(request, db)
