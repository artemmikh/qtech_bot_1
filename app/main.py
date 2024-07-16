from fastapi import FastAPI

# Импортируем роутер.
from starlette.staticfiles import StaticFiles

from app.api.button import router as button
from app.api.render import router as render
from app.api import user_router, render_user
from app.core.config import settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(button)
app.include_router(render)
app.include_router(user_router)
app.include_router(render_user)


@app.on_event('startup')
async def startup():
    await create_first_superuser()
