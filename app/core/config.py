import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Input title in .env'
    database_url: str
    BASE_DIR = Path(__file__).resolve().parent.parent
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')
    PICTURE_ROOT = os.path.join(MEDIA_ROOT, 'pics')
    DOC_ROOT = os.path.join(MEDIA_ROOT, 'docs')
    secret: str = 'SECRET'
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in mins
    COOKIE_NAME = "access_token"
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    COOKIE_NAME: str = "access_token"
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
