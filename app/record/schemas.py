"""Record Pydantic Schemas"""

from typing import Optional, Literal
from datetime import datetime
from pydantic import BaseModel

RecordActionType = Literal["GET", "LIST", "CREATE", "UPDATE", "BATCH_UPDATE", ]

TableType = Literal["USER", "POINT", "ACTIVITY", "FRIEND", "SOCIAL_MEDIA", "GAME_CHARACTER", "RECORD"]


class RecordScehma(BaseModel):  # defaulf = false
    """Record Schema"""

    id: int
    action: RecordActionType
    table: TableType  
    table_id: int
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
    class Config:
        use_enum_values = True


class RecordDetailsSchema(BaseModel):
    record: RecordScehma
    user_id: Optional[int] = None


class RecordCreateDetailsSchema(BaseModel):
    action: RecordActionType
    table: TableType  
    table_id: int
    custom_logs: Optional[dict] = None
    class Config:
        use_enum_values = True


class RecordCreateRequestSchema(BaseModel):
    user_id: int
    access_token: str
    record_details: RecordCreateDetailsSchema


class RecordCreateResponseSchema(BaseModel):
    record_base: RecordDetailsSchema


class RecordRetrievalRequestSchema(BaseModel):
    id: int
    access_token: str
    user_id: Optional[int] = None


class RecordRetrievalResponseSchema(BaseModel):
    record_base: RecordDetailsSchema


# class RecordUpdateByIdRequestSchema(BaseModel):
#     id: int
#     type: str
#     access_token: str
#     record_payload: Optional[RecordCreateDetailsSchema] = None


# class RecordUpdateByUserIdRequestSchema(BaseModel):
#     type: str
#     access_token: str
#     user_id: int
#     record_payload: Optional[RecordCreateDetailsSchema] = None


# class RecordUpdateResponseSchema(BaseModel):
#     record_base: RecordDetailsSchema
