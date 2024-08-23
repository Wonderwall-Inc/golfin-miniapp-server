"""Point app DB models"""

from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.database import Base
from app.user.models import UserModel


class PointModel(Base):
    """ 
    Represents a point entity and defines the structure of the "point" table in the database
    
    Fields:
    - id: An integer column representing the primary key of the "point" table in the database.
    - amount: An integer column representing the total point thet the user has.
    - owner_id: An integer column representing who is the owner of these points.
    - extra_profit_per_hour: An integer column showing that the extra points the user can get based on the level.
    - created_at: A DateTime column representing the time when the point was created.
    - updated_at: A DateTime column representing the time when the point was last updated.
    - owner: A relationship column showing the owner payload of these points.
    """
    
    __tablename__ = "point"
    id = Mapped[int] = mapped_column(Integer, primary_key = True)
    amount = Mapped[int] = mapped_column(Integer, default = 0)
    owner_id = Mapped[int] = mapped_column(Integer, ForeignKey(UserModel.id))

    # affect by unlockings on enhancement (MINE)
    extra_profit_per_hour = Mapped[int] = mapped_column(Integer, default = 0)
    created_at = Mapped[DateTime] = mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)
    owner = relationship("User", back_populates = "point")

    def __repr__(self) -> str:
        return f"<PointModel by {self.id} owned by={self.owner_id}>"
