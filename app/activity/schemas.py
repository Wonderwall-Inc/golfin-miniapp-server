from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ActivityBaseSchema(BaseModel):
    """
    Base schema for Activity
    """

    id: int
    is_logged_in: bool
    login_streak: int
    total_logins: int
    last_action_time: datetime
    last_login_time: datetime
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
