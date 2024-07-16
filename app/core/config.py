import os
from pathlib import Path
from pydantic import BaseSettings, EmailStr
from typing import Optional


_BASE_DIR = Path(__file__).resolve().parent.parent
_STATIC_PICTURE_DIR = 'static/media/pics/'
_STATIC_DOC_DIR = 'static/media/docs/'
_STATIC_PICTURE_ROOT = os.path.join(_BASE_DIR, _STATIC_PICTURE_DIR)
_STATIC_DOC_ROOT = os.path.join(_BASE_DIR, _STATIC_DOC_DIR)

URL_DOMAIN = 'http://127.0.0.1:8000'


class Settings(BaseSettings):
    app_title: str = 'Input title in .env'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'superuser@fake.ru'
    first_superuser_password: Optional[str] = 'secret_password'

    class Config:
        env_file = '.env'


settings = Settings()
