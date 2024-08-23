"""User app DB models"""

from datetime import datetime
from typing import Optional, Set
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy import Integer, String, Boolean, JSON, DateTime, ARRAY

from core.database import Base
from app.character.models import CharacterModel


class UserModel(Base):
    """
    Represents an user entity and defines the structure of the "user" table in the database.

    Fields:
    - id: An integer column representing the primary key of the "user" table.
    - username: A string column representing the username on the telegram.
    - telegram_id: A string column representing the telegram_id on the telegram.
    - token_balance: A integer column representing the total token amount as ton / eth from user coins.
    - is_active: A boolean column representing if the user is inactive or active per every 3 months.
    - is_premium: A boolean column showing if the user is premium telegram user.
    - in_game_items: A dictionary column showing the items which belong to the user.
    - wallet_address: A string column showing the user ton wallet address on telegram.
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - skin: A string column showing the skin of the user
    - chat_id: A string column showing which chat does the user belong to with bot
    - location: A string column showing where is the user.
    - nationality: A string column showing which conuntry the user belong to.
    - age: A string column showing the age of the user.
    - gender: A string column showing the gender of the user.
    - email: A string column showing the email of the user.
    - custom_logs: A dictionary column keeping any unexpected data if emergency.
    - characters: The relationshiop columns showing the type of character of user.
    - sender: A relationship column showing the sender payload if the user is a part of sender a friendship.
    - receiver: A relationship column showing the receiver payload if the user is a part of receiver on a friendship.
    - point: The relationship columns showing all the points of the user.
    - activity: A relationship columns keeping track on the user activity, like daily login.
    - social_media: A relationship column showing which social media are connected by user.
    - access_token: A string column representing the access token of the user. (PENDING)
    """

    __tablename__ = "user"
    id = Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    username = Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    telegram_id = Mapped[str] = mapped_column(String(100), unique = True, nullable = False)
    token_balance = Mapped[int] = mapped_column(Integer, default = 0)
    is_active = Mapped[bool] = mapped_column(Boolean, default = True)
    is_premium = Mapped[bool] = mapped_column(Boolean, default = False)
    wallet_address = Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    in_game_items = Mapped[Optional[dict]] = mapped_column(JSON, nullable = True)
    # access_token: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    created_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)
    
    
    skin = Mapped[list[str]] = mapped_column(ARRAY(String(100)), default = "Default") # affect the reward
    
    chat_id = Mapped[Optional[str]] = mapped_column(String(100),nullable = True)
    # marketing
    location: Mapped[str] = mapped_column(String(100), nullable = False)  # prefecture
    nationality: Mapped[str] = mapped_column(String(100), nullable = False)
    age = Mapped[Optional[int]] = mapped_column(Integer, nullable = True)
    gender = Mapped[Optional[str]] = mapped_column(String(100), nullable = True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable = True)

    custom_logs = Mapped[Optional[dict]] = mapped_column(JSON)

    # multiple character
    characters = Mapped[Set["CharacterModel"]] = relationship(back_populates = "user")

    sender = relationship("FriendModel", foreign_keys = "Friend.sender_id", back_populates = "sender")
    
    receiver = relationship("FriendModel", foreign_keys = "Friend.receiver_id", back_populates = "receiver")

    point = relationship("PointModel", back_populates = "owner")

    activity = relationship("ActivityModel", back_populates = "user")

    social_media = relationship("SocialMediaModel", back_populates = "user")

    # REVIEW: consider if these are ok and can be added at the moment?   
    # gonCoin = relationship("CoinGonModel", back_populates="user")
    # usdtCoin = relationship("CoinUsdtModel", back_populates="user")
    # usdcCoin = relationship("CoinUsdcModel", back_populates="user")
    # tonCoin = relationship("CoinTonModel", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<UserModel telegram id={self.telegram_id} username={self.username}"
