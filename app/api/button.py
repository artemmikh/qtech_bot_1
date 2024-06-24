import shutil

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.button import ButtonBase
from app.core.db import get_async_session
from app.crud.button import button_crud
from app.schemas.button import ButtonCreation

router = APIRouter(
    tags=['API Bottons']
)


@router.post(
    '/api/create'
)
async def create_button(
        name: str,
        location: bool,
        department: bool,
        message: str,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_async_session),
):
    with open('app/static/media/' + file.filename, 'wb+') as image:
        shutil.copyfileobj(file.file, image)

    picture = str('app/static/media' + file.filename)

    new_button = await button_crud.create_with_pic(name=name,
                                                   location=location,
                                                   department=department,
                                                   message=message,
                                                   picture=picture,
                                                   session=session)
    return new_button

@router.get(
    '/api',
    response_model=list[ButtonBase]
)
async def get_all_buttons(
        session: AsyncSession = Depends(get_async_session),
):
    all_buttons = await button_crud.get_multi(session)
    return all_buttons
