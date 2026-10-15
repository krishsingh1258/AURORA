import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret"))
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret")

    # If full DATABASE_URL exists (e.g. from Render or Supabase), prefer it
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Normalize postgres:// to postgresql:// if needed by SQLAlchemy
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        # Ensure it uses psycopg2
        if database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg2://"):
            database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)
        
        # Ensure sslmode=require is present
        if "sslmode=" not in database_url:
            separator = "&" if "?" in database_url else "?"
            database_url = f"{database_url}{separator}sslmode=require"

        SQLALCHEMY_DATABASE_URI = database_url
    else:
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_PORT", "6543")
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_NAME = os.getenv("DB_NAME", "postgres")

        _DB_USER_ENC = quote_plus(DB_USER)
        _DB_PASSWORD_ENC = quote_plus(DB_PASSWORD)

        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg2://{_DB_USER_ENC}:{_DB_PASSWORD_ENC}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
