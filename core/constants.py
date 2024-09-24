"""All Global Constants"""
import os
from dotenv import load_dotenv

load_dotenv()


class Constants:
    """
    Global Constants
    """

    # SQLALCHAMY_DATABASE_URL = "sqlite:///./local.db"

    username = os.environ.get("DB_USER") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_USER")
    password = os.environ.get("DB_PASS") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_PASSWORD")
    port = os.environ.get("DB_PORT") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_PORT")
    dbName = os.environ.get("DB_NAME") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_HOST")
    dbHost = os.environ.get("DB_HOST") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_DATABASE")
    dburl = os.environ.get("MYSQL_CONNECTION_URL") if os.environ.get("PROJECT_ENV") == 'dev' else os.environ.get("TIDB_SQLALCHAMY_DEV_DATABASE_URL")
    
    # tidb_username= os.environ.get("TIDB_USER")
    # tidb_password= os.environ.get("TIDB_PASSWORD")
    # tidb_port= os.environ.get("TIDB_PORT")
    # tidb_db_host= os.environ.get("TIDB_HOST")
    # tidb_database= os.environ.get("TIDB_DATABASE")
    # tidb_sqlalchamy_database_url = os.environ.get("TIDB_SQLALCHAMY_DATABASE_URL")

    # LOCAL
    # SQLALCHAMY_DATABASE_URL = f"mysql+pymysql://{username}:{password}@{dbHost}:{port}/{dbName}"
    
    # REMOTE
    # SQLALCHAMY_DATABASE_URL = f"mysql+pymysql://{tidb_username}:{tidb_password}@{tidb_db_host}:{tidb_port}/{tidb_database}"
    # TIDB_SQLALCHAMY_DATABASE_URL = tidb_sqlalchamy_database_url
    
    # SECRET_KEY = ""
    # ALGORITHM = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES = 30
