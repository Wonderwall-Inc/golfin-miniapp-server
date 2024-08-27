"""Friend app DB models"""

from typing import Literal, get_args, Optional
from sqlalchemy import Integer, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column, backref
from datetime import datetime
from core.database import Base

FriendStatusTpye = Literal["pending", "active", "rejected"]
 
class FriendModel(Base):
    __tablename__ = "friend"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key = True,
        unique = True,
        index = True,
        nullable=False,
        autoincrement=True
    )
    status: Mapped[FriendStatusTpye] = mapped_column(Enum(
        *get_args(FriendStatusTpye), 
        name="friendStatusTpye",  
        create_constraints = True,
        validate_strins = True,
        default = "pending",))

    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    receiver_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default = datetime.now,onupdate = datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

    sender = relationship("UserModel", backref = backref("user_send", uselist = False), foreign_keys = [sender_id])
    receiver = relationship("UserModel",backref = backref("user_receive", uselist = False),foreign_keys = [receiver_id])

    def __repr__(self) -> str:
        return f"<FriendModel id={self.id} sender_id={self.sender_id} receiver_id={self.receiver_id}>"
