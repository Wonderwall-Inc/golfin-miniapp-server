# """Record app DB models"""

# from datetime import datetime
# from sqlalchemy import Integer, ForeignKey, DateTime, JSON, Enum
# from sqlalchemy.orm import mapped_column, Mapped, relationship
# from core.database import Base
# from typing import Optional, Literal, get_args


# RecordActionType = Literal["GET", "LIST", "CREATE", "UPDATE", "BATCH_UPDATE", ]

# TableType = Literal["USER", "POINT", "ACTIVITY", "FRIEND", "SOCIAL_MEDIA", "GAME_CHARACTER", "RECORD"]



# class RecordModel(Base):
#     __tablename__ = "record"
#     id: Mapped[int] = mapped_column(
#         Integer,
#         primary_key=True,
#         unique=True,
#         index=True,
#         nullable=False,
#         autoincrement=True,
#     )
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"),  nullable=False, unique=False)
    
#     # amount: Mapped[int] = mapped_column(Integer, default=0)
#     action: Mapped[RecordActionType] = mapped_column(
#         Enum(
#             *get_args(RecordActionType),
#             name="recordActionType",
#             create_constraints=True,
#             validate_strins=True,
#             default="GET",
#         )
#     )
#     table: Mapped[TableType] = mapped_column(
#         Enum(
#             *get_args(TableType),
#             name="tableType",
#             create_constraints=True,
#             validate_strins=True,
#             default="USER",
#         )
#     )
    
#     table_id: Mapped[int] = mapped_column(Integer, nullable=False)
    
#     created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
#     updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
#     custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

#     user = relationship("UserModel", back_populates="record")

#     def __repr__(self) -> str:
#         return f"<RecordModel by {self.id} owned by={self.user_id}>"
