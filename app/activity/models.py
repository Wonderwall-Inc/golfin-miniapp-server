"""Activity app DB models"""

from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from typing import Optional

class ActivityModel(Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        index=True,
        nullable=False,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, unique=True)
    is_logged_in: Mapped[bool] = mapped_column(default=False, nullable=False)
    login_streak: Mapped[int] = mapped_column(Integer, default=0)
    total_logins: Mapped[int] = mapped_column(Integer, default=0)
    last_action_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_login_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    custom_logs: Mapped[Optional[dict]] = mapped_column(JSON)

    user = relationship("UserModel", back_populates="activity")

    def __repr__(self) -> str:
        return f"<ActivityModel by {self.id} from user {self.user.id}>"
