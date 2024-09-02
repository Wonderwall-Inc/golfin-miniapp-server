import logging
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


def retrieve_point(
    request: schemas.PointRetrivalRequestSchema, db: Session
) -> schemas.PointRetrivalResponseSchema:
    if not request.id or not request.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Id and User Id are required",
        )
    existing_point = db.query(PointModel).filter(PointModel.id == id).first()
    try:
        if not existing_point:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Point with id {request.id} not found",
            )
        return schemas.PointRetrivalResponseSchema(
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
    requests: list[schemas.PointRetrivalRequestSchema], db: Session
) -> list[schemas.PointRetrivalResponseSchema]:
    for request in requests:
        if not request.id or not request.user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Id and User Id are required",
            )
        existing_point = (
            db.query(PointModel).filter(PointModel.id == request.id).first()
        )
        try:
            if not existing_point:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Point with id {id} not found",
                )
            return schemas.PointRetrivalResponseSchema(
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


def update_point(
    type: str, db: Session, request: schemas.PointUpdateRequestSchema
) -> schemas.PointUpdateResponseSchema:  # add and minus
    if not type or not request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type and request are required",
        )
    if type == "add":
        try:
            existing_point = (
                db.query(PointModel).filter(PointModel.id == request.id).first()
            )
            if not existing_point:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Point with id {request.id} not found",
                )
            if request.point_payload:
                if request.point_payload.amount:
                    existing_point.amount += request.point_payload.amount
                if request.point_payload.extra_profit_per_hour:
                    existing_point.extra_profit_per_hour = (
                        request.point_payload.extra_profit_per_hour
                    )

            db.commit()
            db.refresh(existing_point)
            return schemas.PointUpdateResponseSchema(
                point_base=schemas.PointDetailsSchema(
                    user_id=existing_point.user_id,
                    point=schemas.PointScehma(
                        id=existing_point.id,
                        amount=existing_point.amount,
                        extra_profit_per_hour=existing_point.extra_profit_per_hour,
                        created_at=existing_point.created_at,
                        update_point=existing_point.updated_at,
                        custom_logs=existing_point.custom_logs,
                    ),
                )
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")


# def delete_point():
