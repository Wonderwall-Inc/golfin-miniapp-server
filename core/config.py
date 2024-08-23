"""
Global Configuration
"""
from datetime import timedelta
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Base Global Settings
    """

    prod: bool = False
    fastapi_log_level: str = "info"
    # jwt_secret: str = "secret"
    # jwt_algorithm: str = "HS256"
    # jwt_expiration_seconds: float = timedelta(minutes=15).total_seconds()
    # jwt_refresh_expiration_seconds: float = timedelta(weeks=2).total_seconds()
    sentry_dsn: Optional[str] = None


cfg = Settings()
sentry_config = dict(dsn=cfg.sentry_dsn)
