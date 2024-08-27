"""All Global Constants"""
import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    """
    Global Constants
    """

    # SQLALCHAMY_DATABASE_URL = "sqlite:///./local.db"

    username = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    port = os.environ.get("DB_PORT")
    dbName = os.environ.get("DB_NAME")
    dbHost = os.environ.get("DB_HOST")
    dburl = os.environ.get("MYSQL_CONNECTION_URL")

    # TODO: Remote
    SQLALCHAMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{dbHost}:{port}/{dbName}"
    
    # SECRET_KEY = ""
    # ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 30
