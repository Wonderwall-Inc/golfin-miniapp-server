"""Character app DB models"""

from core.database import Base
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, DateTime

from app.user.models import UserModel

class CharacterModel(Base):
    """
    Represents a friend entity and defines the structure of the "character" table in the database.
    
    Fields:
    - id: An integer column representing the primary key of the "character" table.
    - first_name: A string column showing the first name of the character.
    - last_name: A string column showing the last name  of the character.
    - gender: An integer column showing the gender of the character.
    - title: A string column showing the title on the character >>> diff character diff characterStats.
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - user: The relationship column who owns this character.
    - stats: The relationship column showing the detail properties of this character.
    """
    __tablename__="character"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        autoincrement=True
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable = False)
    last_name: Mapped[str] = mapped_column(String(100), nullable = False)
    gender: Mapped[int] = mapped_column(Integer, default=1)
    title = Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # CEO, change to set later on
    created_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)
    user = relationship(UserModel, back_populates = "characters", single_parent = True)
    stats = relationship("CharacterStatsModel", back_populates="character")
    
    def __repr__(self) -> str:
        return f"<CharacterModel 
        first_name={self.first_name} last_name={self.last_name} 
        by {self.user.telegram_id}>"
        
    
class CharacterStatsModel(Base):
    __tablename__ = "character_stats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True,
    )
    character_id: Mapped[int] = mapped_column(ForeignKey(CharacterModel.id), nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1)
    exp_points: Mapped[int] = mapped_column(Integer, default=0)
    stamina: Mapped[int] = mapped_column(Integer, default=0)
    recovery: Mapped[int] = mapped_column(Integer, default=0)
    condition: Mapped[int] = mapped_column(Integer, default=0)
    character: Mapped["CharacterModel"] = relationship(
        "CharacterModel", back_populates="stats", single_parent=True
    )

    __table_args__ = (UniqueConstraint("character_id"),)

    def __repr__(self) -> str:
        return f"<CharacterStatsModel by {self.character.id}>"
