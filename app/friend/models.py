"""Friend app DB models"""

from typing import Literal, get_args
from sqlalchemy import Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, relationship, mapped_column, backref
from datetime import datetime

from app.user.models import UserModel

from core.database import Base

FriendStatusTpye = Literal["pending", "active", "rejected"]

class FriendModel(Base):
    """
    Represents a friend entity and defines the structure of the "friend" table in the database
    
    Fields:
    - id: An integer column representing the primary key of the "friend" table.
    - status: Enum column representing the friendship status.
    - sender_id: An integer column showing which sent the friend code to receiver.
    - receiver_id: An integer column showing which received the friend code from sender.
    - created_at: A datetime column showing the time when the friend was created.
    - updated_at: A datetime column showing the time when the friend was updated.
    - sender: A relationship column showing the sender payload on single friendship.
    - receiver: A relationship column showing the receiver payload on single friendship.
    """
    __tablename__ = "friend"
    id = Mapped[int] = mapped_column(
        Integer, 
        primary_key = True,
        unique = True,
        nullable = False,
        index = True,
        autoincrement = True
    )

    status = Mapped[FriendStatusTpye] = mapped_column(Enum(
        *get_args(FriendStatusTpye), 
        name="friendStatusTpye",  
        create_constraints = True,
        validate_strins = True,
        default = "pending",))

    sender_id = Mapped[int] = mapped_column(Integer, ForeignKey(UserModel.id))
    receiver_id = Mapped[int] = mapped_column(Integer, ForeignKey(UserModel.id))
    created_at = Mapped(datetime)= mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped(datetime)= mapped_column(DateTime,default = datetime.now,onupdate = datetime.now)

    sender = relationship("UserModel", backref = backref("user_send", uselist = False), foreign_keys = [sender_id])
    receiver = relationship("UserModel",backref = backref("user_receive", uselist = False),foreign_keys = [receiver_id])

    def __repr__(self) -> str:
        return f"<FriendModel id={self.id} sender_id={self.sender_id} receiver_id={self.receiver_id}"
