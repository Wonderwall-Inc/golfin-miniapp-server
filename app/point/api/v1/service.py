import logging
from typing import List
from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from app.point.models import PointModel
from app.point import schemas

# from app.user.schemas import UserSchema


def create_point(
    request: schemas.PointCreateRequestSchema, db: Session
) -> schemas.PointCreateResponseSchema:
    if not request.user_id or not request.point_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User id, point details per hour are required",
        )
    if (
        not request.point_details.amount
        or not request.point_details.extra_profit_per_hour
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount and extra profit per hour are required",
        )
    point = db.query(PointModel).filter(PointModel.user_id == request.user_id).first()

    if point:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Point already exists"
        )

    new_point = PointModel(
        user_id=request.user_id,
        amount=request.point_details.amount,
        extra_profit_per_hour=request.point_details.extra_profit_per_hour,
        custom_logs=request.point_details.custom_logs,
    )
    db.add(new_point)
    db.commit()
    db.refresh(new_point)
    return schemas.PointCreateResponseSchema(
        point_base=schemas.PointDetailsSchema(
            point=schemas.PointScehma(
                id=new_point.id,
                amount=new_point.amount,
                extra_profit_per_hour=new_point.extra_profit_per_hour,
                created_at=new_point.created_at,
                updated_at=new_point.updated_at,
                custom_logs=new_point.custom_logs,
            )
        )
    )


def retrieve_point_by_point_id(
    id: int, db: Session
) -> schemas.PointRetrievalResponseSchema:
    if not id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Point id is required",
        )
    existing_point = db.query(PointModel).filter(PointModel.id == id).first()
    if not existing_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Point with id {id} not found",
        )
    try:
        return schemas.PointRetrievalResponseSchema(
            point_base=schemas.PointDetailsSchema(
                user_id=existing_point.user_id,
                point=schemas.PointScehma(
                    id=existing_point.id,
                    amount=existing_point.amount,
                    extra_profit_per_hour=existing_point.extra_profit_per_hour,
                    created_at=existing_point.created_at,
                    updated_at=existing_point.updated_at,
                    custom_logs=existing_point.custom_logs,
                ),
            )
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_point_by_user_id(
    user_id: int, db: Session
) -> schemas.PointRetrievalResponseSchema:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User id is required",
        )
    existing_point = db.query(PointModel).filter(PointModel.id == user_id).first()
    if not existing_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Point with user id {user_id} not found",
        )
    try:
        return schemas.PointRetrievalResponseSchema(
            point_base=schemas.PointDetailsSchema(
                user_id=existing_point.user_id,
                point=schemas.PointScehma(
                    id=existing_point.id,
                    amount=existing_point.amount,
                    extra_profit_per_hour=existing_point.extra_profit_per_hour,
                    created_at=existing_point.created_at,
                    updated_at=existing_point.updated_at,
                    custom_logs=existing_point.custom_logs,
                ),
            )
        )
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_points(
    user_ids: List[int], db: Session
) -> List[schemas.PointRetrievalResponseSchema]:
    if not user_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ids are required",
        )
    else:
        existing_points = (
            db.query(PointModel).filter(PointModel.user_id.in_(user_ids))
            # .options(joinedload(PointModel.user))
            .all()
        )
        return [
            schemas.PointRetrievalResponseSchema(
                point_base=schemas.PointDetailsSchema(
                    user_id=ex.user_id,
                    point=schemas.PointScehma(
                        id=ex.id,
                        amount=ex.amount,
                        extra_profit_per_hour=ex.extra_profit_per_hour,
                        created_at=ex.created_at,
                        updated_at=ex.updated_at,
                        custom_logs=ex.custom_logs,
                    ),
                )
            )
            for ex in existing_points
        ]


def update_point_by_id(request: schemas.PointUpdateByIdRequestSchema, db: Session):  # add and minus
    if not request or not request.type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type and request are required",
        )
    existing_point = db.query(PointModel).filter(PointModel.id == request.id).first()
    if not existing_point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Point with user_id {request.id} not found",
        )
    if request.point_payload:
        if request.point_payload.amount:
            if request.type == 'add':
                existing_point.amount += request.point_payload.amount
            if request.type == 'minus':
                existing_point.amount -= request.point_payload.amount
            else:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                    detail=f"Method not allowed"
                )
        if request.point_payload.extra_profit_per_hour:
            existing_point.extra_profit_per_hour = request.point_payload.extra_profit_per_hour
    db.commit()
    db.refresh(existing_point)
    return schemas.PointUpdateResponseSchema(
        point_base=schemas.PointDetailsSchema(
            point=schemas.PointScehma(
                id=existing_point.id,
                amount=existing_point.amount,
                extra_profit_per_hour=existing_point.extra_profit_per_hour,
                created_at=existing_point.created_at,
                updated_at=existing_point.updated_at,
                custom_logs=existing_point.custom_logs,
            )
        )
    )

# REVIEW: def delete_point(), batch update
