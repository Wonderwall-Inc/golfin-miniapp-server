"""Point app DB models"""

from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core.database import Base
from typing import Optional

class PointModel(Base):
    __tablename__ = "point"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    
    # amount: Mapped[int] = mapped_column(Integer, default=0)
    login_amount: Mapped[int] = mapped_column(Integer, default=0)
    referral_amount: Mapped[int] = mapped_column(Integer, default=0)
    
    extra_profit_per_hour: Mapped[int] = mapped_column(Integer, default=0)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

    user = relationship("UserModel", back_populates="point")

    def __repr__(self) -> str:
        return f"<PointModel by {self.id} owned by={self.user_id}>"
