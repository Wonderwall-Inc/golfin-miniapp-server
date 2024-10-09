"""Game Character App Business Logics"""
import logging
import pytz
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.game_character import schemas
from app.game_character.models import GameCharacterModel, GameCharacterStatsModel

def create_game_character(request: schemas.GameCharacterCreateRequestSchema, db: Session) -> schemas.GameCharacterCreateResponseSchema:
    """Create New Game Character"""
    if not request.user_id or not request.character_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User id and character_details are required")
    if not request.character_details.first_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing first_name")
    if not request.character_details.last_name:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing last_name")
    if not request.character_details.gender:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing gender")
    if not request.character_details.title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="missing title")
    
    try:
        game_character = (
            db.query(GameCharacterModel).filter(
                GameCharacterModel.first_name.ilike(request.character_details.first_name),
                GameCharacterModel.last_name.ilike(request.character_details.last_name),
            )
            .first()
        )
    
        if game_character and game_character.user_id == request.user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Character with same name already exists")

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

        return schemas.GameCharacterCreateResponseSchema(
            game_character_id=new_game_character.id,
            character_stats=schemas.GameCharacterStatsSchema(
                id=stats.id,
                level=stats.level,
                exp_points=stats.exp_points,
                stamina=stats.stamina,
                recovery=stats.recovery,
                condition=stats.recovery,
                created_at=stats.created_at.astimezone(pytz.timezone('Asia/Singapore')) if stats.created_at else None,
                updated_at=stats.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if stats.updated_at else None,
                custom_logs=stats.custom_logs,
            ),
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")  


def retrieve_game_character(game_character_id: Optional[int], user_id: Optional[int], db: Session)-> List[schemas.GameCharacterCreateResponseSchema]:
    """Retrieve Game Character Details from Single User"""
    if not game_character_id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Missing id or game character id")
    
    try:
        base_query = db.query(GameCharacterModel)
        filters = []

        if game_character_id is not None:
            filters.append(GameCharacterModel.id == game_character_id)

        if user_id is not None:
            filters.append(GameCharacterModel.user_id == user_id)

        if filters:
            existing_characters = base_query.filter(*filters).all()

            if not existing_characters:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Game Character with id {game_character_id} not found")

            return [
                schemas.GameCharacterRetrievalResponseSchema(
                    character_details=schemas.GameCharacterDetailsSchema(
                        game_character_base=schemas.GameCharacterSchema(
                            id=game_character.id,
                            first_name=game_character.first_name,
                            last_name=game_character.last_name,
                            gender=game_character.gender,
                            title=game_character.title,
                            created_at=game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if game_character.created_at else None,
                            updated_at=game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if game_character.updated_at else None,
                            custom_logs=game_character.custom_logs,
                        )
                    ),
                    character_stats=[
                        schemas.GameCharacterStatDetailsSchema(
                            game_character_id=stat.game_character_id,
                            game_character_stat_base=schemas.GameCharacterStatsSchema(
                                id=stat.id,
                                level=stat.level,
                                exp_points=stat.exp_points,
                                stamina=stat.stamina,
                                recovery=stat.recovery,
                                condition=stat.condition,
                                created_at=stat.created_at.astimezone(pytz.timezone('Asia/Singapore')) if stat.created_at else None,
                                updated_at=stat.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if stat.updated_at else None,
                                custom_logs=stat.custom_logs,
                            ),
                        )
                        for stat in game_character.stats
                    ]
                )
                for game_character in existing_characters
            ]
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_game_character_stat(id: Optional[int], game_character_id: Optional[int], db: Session) -> schemas.GameCharacterStatRetrievalResponseSchema:
    """Retrieve Game Character Stats from Single Character"""
    if not id and not game_character_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing required parameters")
    
    try:
        base_query = db.query(GameCharacterStatsModel)
        filters = []

        if id is not None:
            filters.append(GameCharacterStatsModel.id==id)

        if game_character_id is not None:
            filters.append(GameCharacterStatsModel.game_character_id==game_character_id)

        if filters:
            existing_stats = base_query.filter(*filters).first()
            if not existing_stats or existing_stats is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Game Character Stat not found")
            
            return schemas.GameCharacterStatRetrievalResponseSchema(
                game_character_id=existing_stats.game_character_id,
                character_stats=schemas.GameCharacterStatsSchema(
                    id=existing_stats.id,
                    level=existing_stats.level,
                    exp_points=existing_stats.exp_points,
                    stamina=existing_stats.stamina,
                    recovery=existing_stats.recovery,
                    condition=existing_stats.condition,
                    created_at=existing_stats.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_stats.created_at else None,
                    updated_at=existing_stats.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_stats.updated_at else None,
                    custom_logs=existing_stats.custom_logs,
                    ),
                )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_game_character_all_list(db: Session, user_ids: List[int], skip: int = 0, limit: int = 15) -> List[schemas.GameCharacterCreateResponseSchema]:
    """Retrieve Game Character List from all Users"""
    try:
        if user_ids:
            existing_game_characters = db.query(GameCharacterModel).filter(GameCharacterModel.user_id.in_(user_ids)).offset(skip).limit(limit).all()
        else:
            existing_game_characters = db.query(GameCharacterModel).offset(skip).limit(limit).all()
        return [
            schemas.GameCharacterRetrievalResponseSchema(
                character_details=schemas.GameCharacterDetailsSchema(
                    game_character_base=schemas.GameCharacterSchema(
                        id=existing_game_character.id, 
                        first_name=existing_game_character.first_name,
                        last_name=existing_game_character.last_name,
                        gender=existing_game_character.gender,
                        title=existing_game_character.title,
                        created_at=existing_game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_game_character.created_at else None,
                        updated_at=existing_game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_game_character.updated_at else None,
                        custom_logs=existing_game_character.custom_logs,
                    )
                ),
                character_stats=[
                    schemas.GameCharacterStatDetailsSchema(
                        game_character_id=stat.game_character_id,
                        game_character_stat_base=schemas.GameCharacterStatsSchema(
                            id=stat.id,
                            level=stat.level,
                            exp_points=stat.exp_points,
                            stamina=stat.stamina,
                            recovery=stat.recovery,
                            condition=stat.condition,
                            created_at=stat.created_at.astimezone(pytz.timezone('Asia/Singapore')) if stat.created_at else None,
                            updated_at=stat.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if stat.updated_at else None,
                            custom_logs=stat.custom_logs,
                        ),
                    )
                    for  stat in existing_game_character.stats
                ]
            )

            for existing_game_character in existing_game_characters
        ]
    except Exception as e:
        logging.error(f"An error occured: {e}")
      
  
def retrieve_game_character_list_from_one_user(db: Session, user_id: int, skip: int = 0, limit: int = 15) -> List[schemas.GameCharacterSchema]:
    """Retrieve all Game Characters from Single User"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing user id")
    try:
        existing_game_characters = db.query(GameCharacterModel).filter(GameCharacterModel.user_id==user_id).offset(skip).limit(limit).all()
        return [
            schemas.GameCharacterSchema(
                id=existing_game_character.id,
                first_name=existing_game_character.first_name,
                last_name=existing_game_character.last_name,
                gender=existing_game_character.gender,
                title=existing_game_character.title,
                created_at=existing_game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_game_character.created_at else None,
                updated_at=existing_game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if existing_game_character.updated_at else None,
                custom_logs=existing_game_character.custom_logs,
            )
            for existing_game_character in existing_game_characters
        ]
    except Exception as e:
        logging.error(f"An error occured: {e}")


def update_game_character(request: schemas.GameCharacterUpdateRequestSchema, db: Session) -> schemas.GameCharacterUpdateResponseSchema:
    """Update a Game Character with Stats"""
    if not request or not request.game_character_id:
        raise HTTPException(status_code=400, detail="Game Character ID are required")
    try:
        game_character = db.query(GameCharacterModel).filter(GameCharacterModel.id == request.game_character_id).first()
        
        stats = db.query(GameCharacterStatsModel).filter(GameCharacterStatsModel.game_character_id == request.game_character_id).first()

        if not game_character or not stats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Game Character with id {request.game_character_id} not found")
        
        if request.character_details:
            for field, value in request.character_details.model_dump(exclude_unset=True).items():
                if hasattr(game_character, field):
                    setattr(game_character, field, value)
                
        if request.character_stats:
            for field, value in request.character_stats.model_dump(exclude_unset=True).items():
                if hasattr(stats, field):
                    setattr(stats, field, value)
        
        db.commit()
        db.refresh(game_character)
        db.refresh(stats)
        
        return schemas.GameCharacterUpdateResponseSchema(
            character_details=schemas.GameCharacterSchema(
                id=game_character.id,
                first_name=game_character.first_name,
                last_name=game_character.last_name,
                gender=game_character.gender,
                title=game_character.title,
                created_at=game_character.created_at.astimezone(pytz.timezone('Asia/Singapore')) if game_character.created_at else None,
                updated_at=game_character.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if game_character.updated_at else None,
                custom_logs=game_character.custom_logs,
            ),
            character_stats=schemas.GameCharacterStatsSchema(
                id=stats.id,
                level=stats.level,
                exp_points=stats.exp_points,
                stamina=stats.stamina,
                recovery=stats.recovery,
                condition=stats.condition,
                created_at=stats.created_at.astimezone(pytz.timezone('Asia/Singapore')) if stats.created_at else None,
                updated_at=stats.updated_at.astimezone(pytz.timezone('Asia/Singapore')) if stats.updated_at else None,
                custom_logs=stats.custom_logs,
            )
        )
    except Exception as e:
        logging.error(f"An error occured: {e}")


def delete_game_character(id: int, db: Session):
    """Delete Game Character"""
    try:
        db_game_character = db.query(GameCharacterModel).filter(GameCharacterModel.id == id).first()
        
        if db_game_character:
            db.delete(db_game_character)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game Character {id} not found")
        
    except Exception as e:
        logging.error(f"An error occured: {e}")
