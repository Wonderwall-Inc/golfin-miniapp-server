"""Activity app DB models"""

from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from app.user.models import UserModel


class ActivityModel(Base):
    """
    Represents an activity entity and defines the structures of the "activity" table in the database

    Fields:
    - id: An integer column representing the primary key of the "activity" table.
    - is_logged_in: An boolena column showing if the user is logged in right now.
    - login_streak: An integer column showing the day that user logged in continously.
    - total_logins: An integer column showing the total login time of the user, +1 for each login time # REVIEW how long does it count as a login?
    - last_action_time: A dateime column showing when did the user trigger the action, if no action more than 2 hrs >>> inactive or force logout 
    - last_login_time: A dateime column showing when did the user login to the app
    - created_at: A datetime column showing the time when the user was created.
    - updated_at: A datetime column showing the time when the user was updated.
    - user: The relationship column the user of this activity refer to

    """

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        nullable=False,
        index=True,
        autoincrement=True
    )
   
    is_logged_in= Mapped[bool] = mapped_column(Boolean, default = False)
    login_streak = Mapped[int] = mapped_column(Integer, default = 0)
    total_logins = Mapped[int] = mapped_column(Integer,default = 0)
    last_action_time = Mapped[datetime] = mapped_column(DateTime,nullable = False)
    last_login_time = Mapped[datetime] = mapped_column(DateTime,nullable = False)

    created_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    updated_at = Mapped[datetime] = mapped_column(DateTime, default = datetime.now, onupdate = datetime.now)
    
    user = relationship(UserModel, back_populates="activity")
    
    def __repr__(self) -> str:
        return f"<ActivityModel by {self.id} from user {self.user.id}>"
