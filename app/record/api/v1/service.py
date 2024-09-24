"""Record App Business Logics"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.record import schemas
from app.record.models import RecordModel

def create_record(request: schemas.RecordCreateRequestSchema, db: Session) -> schemas.RecordCreateResponseSchema:
    """Create Record"""
    if not request.user_id or not request.record_details:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id, record details are required")
    
    # if not request.record_details.amount or not request.record_details.extra_profit_per_hour:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount and extra profit per hour are required")
    
    try:
        record = db.query(RecordModel).filter(RecordModel.user_id == request.user_id).first()

        if record:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Record already exists")

        new_record = RecordModel(
            user_id=request.user_id,
            action=request.record_details.action,
            table=request.record_details.table,
            table_id=request.record_details.table_id,
            custom_logs=request.record_details.custom_logs,
        )

        db.add(new_record)
        db.commit()
        db.refresh(new_record)

        return schemas.RecordCreateResponseSchema(
            record_base=schemas.RecordDetailsSchema(
                record=schemas.RecordScehma(
                    id=new_record.id,
                    action=new_record.action,
                    table=new_record.table,
                    table_id=new_record.table_id,
                    created_at=new_record.created_at,
                    updated_at=new_record.updated_at,
                    custom_logs=new_record.custom_logs,
                )
            )
        )
        
    except Exception as e:
        logging.error(f"An error occured: {e}")


def retrieve_record(id: Optional[int], user_id: Optional[int], db: Session) -> schemas.RecordRetrievalResponseSchema:
    """Retrieve Record Details from Single User"""
    if not id and not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Missing id or user_id")
    
    try:
        base_query = db.query(RecordModel)
        filters = []
    
        if id is not None: 
            filters.append(RecordModel.id == id)

        if user_id is not None:
            filters.append(RecordModel.user_id == user_id)

        if filters: 
            existing_record = base_query.filter(*filters).first()
            
            if not existing_record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Record not found")
            
            return schemas.RecordRetrievalResponseSchema(
                record_base=schemas.RecordDetailsSchema(
                    user_id=existing_record.user_id,
                    record=schemas.RecordScehma(
                        id=existing_record.id,
                        action=existing_record.action,
                        table=existing_record.table,
                        table_id=existing_record.table_id,
                        created_at=existing_record.created_at,
                        updated_at=existing_record.updated_at,
                        custom_logs=existing_record.custom_logs,
                    ),
                )
            )
    except Exception as e:
        logging.error(f"An error occurred: {e}")  


def retrieve_record_by_user_id(user_id: int, db: Session) -> schemas.RecordRetrievalResponseSchema:
    """Retrieve Record Details from Single User by user_id"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id is required")
    
    try:
        existing_record = db.query(RecordModel).filter(RecordModel.id == user_id).first()
    
        if not existing_record:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with user id {user_id} not found")
    
        return schemas.RecordRetrievalResponseSchema(
            record_base=schemas.RecordDetailsSchema(
                user_id=existing_record.user_id,
                record=schemas.RecordScehma(
                    id=existing_record.id,
                    action=existing_record.action,
                    table=existing_record.table,table_id=existing_record.table_id,
                    created_at=existing_record.created_at,
                    updated_at=existing_record.updated_at,
                    custom_logs=existing_record.custom_logs,
                ),
            )
        )

    except Exception as e:
        logging.error(f"An error occurred: {e}")


def retrieve_record_list(db: Session, user_ids: List[int], skip: int = 0, limit: int = 15) -> List[schemas.RecordRetrievalResponseSchema]:
    """Retrieve Records by List from Multiple Users"""
    try:
        if user_ids:
            existing_records = db.query(RecordModel).filter(RecordModel.user_id.in_(user_ids)).offset(skip).limit(limit).all()
        else:
            existing_records = db.query(RecordModel).offset(skip).limit(limit).all()
        
        return [
            schemas.RecordRetrievalResponseSchema(
                record_base=schemas.RecordDetailsSchema(
                    user_id=ex.user_id,
                    record=schemas.RecordScehma(
                        id=ex.id,
                        action=ex.action,
                        table=ex.table,
                        table_id=ex.table_id,
                        created_at=ex.created_at,
                        updated_at=ex.updated_at,
                        custom_logs=ex.custom_logs,
                    ),
                )
            )
            for ex in existing_records
        ]
        
    except Exception as e:
            logging.error(f"An error occurred: {e}")


# def update_record(request: schemas.RecordUpdateByIdRequestSchema, db: Session) -> schemas.RecordUpdateResponseSchema:
#     """Update Record"""
#     if not request or not request.type:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type and request are required")
    
#     try:
#         existing_record = db.query(RecordModel).filter(RecordModel.id == request.id).first()

#         if not existing_record:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with user_id {request.id} not found")

#         if request.type == "add":
#             if request.record_payload.login_amount:
#                 existing_record.login_amout += request.record_payload.login_amount
#             if request.record_payload.referral_amount:
#                 existing_record.referral_amount += request.record_payload.referral_amount
#             if request.record_payload.extra_profit_per_hour: # can be add or minus for that
#                 existing_record.extra_profit_per_hour += request.record_payload.extra_profit_per_hour

#         elif request.type == "minus":
#             if request.record_payload.login_amount:
#                 existing_record.login_amout -= request.record_payload.login_amount
#             if request.record_payload.login_amount:
#                 existing_record.referral_amount -= request.record_payload.referral_amount
#             if request.record_payload.extra_profit_per_hour: # can be add or minus for that
#                 existing_record.extra_profit_per_hour -= request.record_payload.extra_profit_per_hour
#         else:
#             raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"Method not allowed")    

    
#         db.commit()
#         db.refresh(existing_record)
        
#         return schemas.RecordUpdateResponseSchema(
#             record_base=schemas.RecordDetailsSchema(
#                 record=schemas.RecordScehma(
#                     id=existing_record.id,
#                     login_amount=existing_record.login_amout,
#                     referral_amount=existing_record.referral_amount,
#                     extra_profit_per_hour=existing_record.extra_profit_per_hour,
#                     created_at=existing_record.created_at,
#                     updated_at=existing_record.updated_at,
#                     custom_logs=existing_record.custom_logs,
#                 ),
#             user_id=existing_record.user_id
#             )
#         )
        
#     except Exception as e:
#         logging.error(f"An error occurred: {e}")


def delete_record(id: int, db:Session):
    """Delete Record"""
    try:
        db_record = db.query(RecordModel).filter(RecordModel.id == id).first()
        
        if db_record:
            db.delete(db_record)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record {id} not found")
        
    except Exception as e:
        logging.error(f"An error occured: {e}")

    

# REVIEW: delete_record, batch update
