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

    SQLALCHAMY_DATABASE_URL = (
        f"mysql+pymysql://{username}:{password}@{dbHost}:{port}/{dbName}"
    )

    print(SQLALCHAMY_DATABASE_URL)
    # SECRET_KEY = ""
    # ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 30
