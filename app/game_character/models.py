"""Character app DB models"""

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, DateTime, JSON
from core.database import Base
from typing import Optional

class GameCharacterModel(Base):
    __tablename__ = "game_character"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, unique=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(100), nullable=False) # FIXME: Enum
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)
    
    user = relationship("UserModel", back_populates="game_characters", single_parent=True)
    stats = relationship("GameCharacterStatsModel", back_populates="game_character")

    def __repr__(self) -> str:
        return f"<CharacterModel first_name={self.first_name} by {self.user_id}>"


class GameCharacterStatsModel(Base):
    __tablename__ = "game_character_stats"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        unique=True, 
        index=True, 
        nullable=False,
        autoincrement=True,
    )
    game_character_id: Mapped[int] = mapped_column(ForeignKey("game_character.id"), nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1)
    exp_points: Mapped[int] = mapped_column(Integer, default=0)
    stamina: Mapped[int] = mapped_column(Integer, default=0)
    recovery: Mapped[int] = mapped_column(Integer, default=0)
    condition: Mapped[int] = mapped_column(Integer, default=0) # how to use int to represent as condition?
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)
    
    game_character: Mapped["GameCharacterModel"] = relationship("GameCharacterModel", back_populates="stats", single_parent=True)

    __table_args__ = (UniqueConstraint("game_character_id"),)

    def __repr__(self) -> str:
        return f"<GameCharacterStatsModel by {self.game_character_id}>"
