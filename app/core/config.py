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


    class Config:
        env_file = '.env'

settings = Settings()