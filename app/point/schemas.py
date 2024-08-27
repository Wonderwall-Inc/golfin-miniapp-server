from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PointBaseSchema(BaseModel):
    """
    Base schema for Point
    """

    id: int
    amount: int  # Assuming gender is an integer
    extra_profit_per_hour: int
    created_at: datetime
    updated_at: datetime
    custom_logs: Optional[dict] = None
