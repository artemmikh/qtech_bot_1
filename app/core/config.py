import os
from pathlib import Path
from pydantic import BaseSettings


_BASE_DIR = Path(__file__).resolve().parent.parent
_STATIC_PICTURE_DIR = 'static/media/pics/'
_STATIC_DOC_DIR = 'static/media/docs/'
_STATIC_PICTURE_ROOT = os.path.join(_BASE_DIR, _STATIC_PICTURE_DIR)
_STATIC_DOC_ROOT = os.path.join(_BASE_DIR, _STATIC_DOC_DIR)


class Settings(BaseSettings):
    app_title: str = 'Input title in .env'
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()
