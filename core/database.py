"""
Database Connection & Engine Creation
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from core.constants import Constants

engine = create_engine(Constants.SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


metadata = Base.metadata


def get_db():
    """Get Database Instance"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
