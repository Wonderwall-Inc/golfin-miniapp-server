"""
Database Connection & Engine Creation
"""
import os
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from core.constants import Constants

# LOCAL
# engine = create_engine(Constants.SQLALCHAMY_DATABASE_URL)

# REMOTE 
# engine = create_engine(
#      URL.create(
#             drivername="mysql+pymysql",
#             username=Constants.tidb_username,
#             password=Constants.tidb_password,
#             host=Constants.tidb_db_host,
#             port=Constants.tidb_port,
#             database=Constants.tidb_database
#         ),
#         connect_args={},
# )

# engine_sql = Constants.SQLALCHAMY_DATABASE_URL if os.environ.get("PROJECT_ENV") else Constants.TIDB_SQLALCHAMY_DATABASE_URL
# print(engine_sql)
print(Constants.dburl)
engine = create_engine(
    Constants.dburl, 
    connect_args={"init_command": "SET SESSION time_zone='+08:00'"} # set UTC+8 timezone with Asia/Singapore
)

print(os.environ.get("PROJECT_ENV"))

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
