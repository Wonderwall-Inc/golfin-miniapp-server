import logging
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.game_character.models import GameCharacterModel, GameCharacterStatsModel
from app.game_character.schemas import (
    GameCharacterStatsSchema,
    GameCharacterSchema,
    GameCharacterDetailsSchema,
    GameCharacterStatDetailsSchema,
    GameCharacterCreateRequestSchema,
    GameCharacterCreateResponseSchema,
    GameCharacterRetrievalResponseSchema,
    GameCharacterStatRetrievalResponseSchema,
    GameCharacterUpdateRequestSchema,
    GameCharacterUpdateResponseSchema,
    GameCharacterBaseSchema,
    GameCharacterStatBaseSchema,
    GameCharacterCreateDetailsSchema,
    GameCharacterUpdateDetailsSchema,
    GameCharacterStatsUpdateDetailsSchema,
    GameCharacterRetrievalRequestSchema,
    GameCharacterStatRetrievalRequestSchema,
)

# from core.utils import GameCharacterSchemaFactory


def create_game_character(
    request: GameCharacterCreateRequestSchema, db: Session
) -> GameCharacterCreateResponseSchema:
    """Create New Game Character"""
    if not request.user_id or not request.character_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User id and character_details are required",
        )
    if not request.character_details.first_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing first_name"
        )
    if not request.character_details.last_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing last_name"
        )
    if not request.character_details.gender:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing gender"
        )
    if not request.character_details.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="missing title"
        )
    game_character = (
        db.query(GameCharacterModel)
        .filter(
            GameCharacterModel.first_name.ilike(request.character_details.first_name),
            GameCharacterModel.last_name.ilike(request.character_details.last_name),
        )
        .first()
    )
    if game_character and game_character.user_id == request.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Character with same name already exists",
        )
    new_game_character = GameCharacterModel(
        first_name=request.character_details.first_name,
        last_name=request.character_details.last_name,
        gender=request.character_details.gender,
        title=request.character_details.title,
        user_id=request.user_id,
        custom_logs=request.character_details.custom_logs,
    )
    stats = GameCharacterStatsModel(game_character=new_game_character)
    db.add(new_game_character)
    db.add(stats)
    db.commit()
    db.refresh(new_game_character)

    return GameCharacterCreateResponseSchema(
        game_character_id=new_game_character.id,
        character_stats=GameCharacterStatsSchema(
            id=stats.id,
            level=stats.level,
            exp_points=stats.exp_points,
            stamina=stats.stamina,
            recovery=stats.recovery,
            condition=stats.recovery,
            created_at=stats.created_at,
            updated_at=stats.updated_at,
            custom_logs=stats.custom_logs,
        ),
    )


# FIXME: allow the user id for filtering
def retrieve_game_character(game_character_id: int, db: Session):
    # -> GameCharacterCreateResponseSchema:
    """Retrieve game character by id"""
    if not game_character_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game Character id is requestesd",
        )
    existing_character = (
        db.query(GameCharacterModel)
        .filter(GameCharacterModel.id == game_character_id)
        .first()
    )
    if not existing_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game Character with id {game_character_id} not found",
        )
    stats_payload = [
        GameCharacterStatDetailsSchema(
            game_character_id=stat.game_character_id,
            game_character_stat_base=GameCharacterStatsSchema(
                id=stat.id,
                level=stat.level,
                exp_points=stat.exp_points,
                stamina=stat.stamina,
                recovery=stat.recovery,
                condition=stat.condition,
                created_at=stat.created_at,
                updated_at=stat.updated_at,
                custom_logs=stat.custom_logs,
            ),
        )
        for stat in existing_character.stats
    ]

    try:
        return GameCharacterRetrievalResponseSchema(
            character_details=GameCharacterDetailsSchema(
                game_character_base=GameCharacterSchema(
                    id=existing_character.id,
                    first_name=existing_character.first_name,
                    last_name=existing_character.last_name,
                    gender=existing_character.gender,
                    title=existing_character.title,
                    created_at=existing_character.created_at,
                    updated_at=existing_character.updated_at,
                    custom_logs=existing_character.custom_logs,
                )
            ),
            character_stats=stats_payload,
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


# FIXME: allow character_id for filtering
def retrieve_game_character_stat(
    game_character_id: int, db: Session
) -> GameCharacterStatRetrievalResponseSchema:
    """Retrieve Game Character Stats of single character"""
    if not game_character_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game Character id is requestesd",
        )
    existing_stats = (
        db.query(GameCharacterStatsModel)
        .filter(GameCharacterStatsModel.game_character_id == game_character_id)
        .first()
    )

    if not existing_stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character Stats with id {game_character_id} not found",
        )
    try:
        return GameCharacterStatRetrievalResponseSchema(
            game_character_id=existing_stats.game_character_id,
            character_stats=GameCharacterStatsSchema(
                id=existing_stats.id,
                level=existing_stats.level,
                exp_points=existing_stats.exp_points,
                stamina=existing_stats.stamina,
                recovery=existing_stats.recovery,
                condition=existing_stats.condition,
                created_at=existing_stats.created_at,
                updated_at=existing_stats.updated_at,
                custom_logs=existing_stats.custom_logs,
            ),
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_game_character_list(
    db: Session, user_id: int, skip: int = 0, limit: int = 15
) -> List[GameCharacterSchema]:
    """Retrieve all game characters of single user"""
    game_characters = (
        db.query(GameCharacterModel)
        .filter(GameCharacterModel.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        GameCharacterSchema(
            id=game_character.id,
            first_name=game_character.first_name,
            last_name=game_character.last_name,
            gender=game_character.gender,
            title=game_character.title,
            created_at=game_character.created_at,
            updated_at=game_character.updated_at,
            custom_logs=game_character.custom_logs,
        )
        for game_character in game_characters
    ]


def update_game_character(request: GameCharacterUpdateRequestSchema, db: Session):
    """Update a game character with stats"""
    game_character = (
        db.query(GameCharacterModel)
        .filter(GameCharacterModel.id == request.game_character_id)
        .first()
    )
    stats = (
        db.query(GameCharacterStatsModel)
        .filter(GameCharacterStatsModel.game_character_id == request.game_character_id)
        .first()
    )

    if not game_character or not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game Character with id {request.game_character_id} not found",
        )

    if request.character_details:
        game_character.first_name = request.character_details.first_name
        game_character.last_name = request.character_details.last_name
        game_character.gender = request.character_details.gender
        game_character.title = request.character_details.title
        game_character.custom_logs = request.character_details.custom_logs

    if request.character_stats:
        stats.level = request.character_stats.level
        stats.exp_points = request.character_stats.exp_points
        stats.stamina = request.character_stats.stamina
        stats.recovery = request.character_stats.recovery
        stats.condition = request.character_stats.condition
        stats.custom_logs = request.character_stats.custom_logs

    db.commit()
    db.refresh(game_character)
    db.refresh(stats)
    return GameCharacterUpdateResponseSchema(
        character_details=GameCharacterSchema(
            id=game_character.id,
            first_name=game_character.first_name,
            last_name=game_character.last_name,
            gender=game_character.gender,
            title=game_character.title,
            custom_logs=game_character.custom_logs,
            created_at=game_character.created_at,
            updated_at=game_character.updated_at,
        ),
        character_stats=GameCharacterStatsSchema(
            id=stats.id,
            level=stats.level,
            exp_points=stats.exp_points,
            stamina=stats.stamina,
            recovery=stats.recovery,
            condition=stats.condition,
            custom_logs=stats.custom_logs,
            created_at=stats.created_at,
            updated_at=stats.updated_at,
        ),
    )


def delete_game_character(id: int, db: Session):
    """Delete the game character"""
    db_game_character = (
        db.query(GameCharacterModel).filter(GameCharacterModel.id == id).first()
    )
    if db_game_character:
        db.delete(db_game_character)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game Character {id} not found",
        )


# REVIEW: see if we need
def retrieve_all_game_characters_info(
    db: Session, skip: int = 0, limit: int = 15
) -> List[GameCharacterRetrievalResponseSchema]:
    """Retrieve all game characters of single user"""
    game_characters = db.query(GameCharacterModel).offset(skip).limit(limit).all()
    return [
        GameCharacterRetrievalResponseSchema(
            character_details=GameCharacterDetailsSchema(
                game_character_base=GameCharacterSchema(
                    id=game_character.id,
                    first_name=game_character.first_name,
                    last_name=game_character.last_name,
                    gender=game_character.gender,
                    title=game_character.title,
                    created_at=game_character.created_at,
                    updated_at=game_character.updated_at,
                    custom_logs=game_character.custom_logs,
                )
            ),
            character_stats=[
                GameCharacterStatDetailsSchema(
                    game_character_stat_base=GameCharacterStatsSchema(
                        id=stat.id,
                        level=stat.level,
                        exp_points=stat.exp_points,
                        stamina=stat.stamina,
                        recovery=stat.recovery,
                        condition=stat.condition,
                        custom_logs=stat.custom_logs,
                        created_at=stat.created_at,
                        updated_at=stat.updated_at,
                    ),
                    game_character_id=stat.game_character_id,
                )
                for stat in game_character.stats
            ],
        )
        for game_character in game_characters
    ]
