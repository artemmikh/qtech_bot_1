import os
from pathlib import Path
import uuid
import shutil
from typing import List

from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import (
    _STATIC_PICTURE_DIR, _STATIC_DOC_DIR, _STATIC_PICTURE_ROOT,
    _STATIC_DOC_ROOT
)
from app.schemas.button import ButtonDatabase  # ButtonBase
from app.core.db import get_async_session
from app.crud.button import button_crud
from app.models.button import Button
from app.validators.validators import (
    check_buttons_name_duplicate, check_button_exists
)


router = APIRouter(
    tags=['API Bottons']
)

current_working_directory = os.getcwd()


@router.post(
    '/api/create'
)
async def create_button(
        name: str,
        is_moscow: bool,
        text: str,
        is_department: bool,
        is_active: bool,
        file_pic: list[UploadFile] = File(...),
        file_doc: list[UploadFile] = File(...),
        session: AsyncSession = Depends(get_async_session),
):
    pictures, files = '', ''
    # picture = []
    Path(current_working_directory + '/app/static/media/pics/').mkdir(parents=True, exist_ok=True)
    for pic in file_pic:
        if pic.filename:
            # filename = str(pic.filename).replace(' ', '_')
            filename = str(uuid.uuid4()) + str(pic.filename)
            with open(current_working_directory + '/app/static/media/pics/' + filename, 'wb') as image:
                shutil.copyfileobj(pic.file, image)
            # picture.append('static/media/pics/' + filename)
            pictures += ' ' + _STATIC_PICTURE_DIR + filename

    # picture = ' '.join(picture)

    # item = []
    Path(current_working_directory + '/app/static/media/docs/').mkdir(parents=True, exist_ok=True)
    for doc in file_doc:
        if doc.filename:
            # filename = str(doc.filename).replace(' ', '_')
            filename = str(uuid.uuid4()) + str(doc.filename)
            with open(current_working_directory + '/app/static/media/docs/' + filename, 'wb') as file:
                shutil.copyfileobj(doc.file, file)
            # item.append('static/media/docs/' + filename)
            files += ' ' + _STATIC_DOC_DIR + filename

    # file = ' '.join(item)

    new_button = await button_crud.create_with_pic(name=name,
                                                   is_moscow=is_moscow,
                                                   text=text,
                                                   # picture=picture,
                                                   picture=pictures,
                                                   # file=file,
                                                   file=files,
                                                   is_department=is_department,
                                                   is_active=is_active,
                                                   session=session)
    return new_button


@router.get(
    '/api',
    response_model=list[ButtonDatabase],
    response_model_exclude_none=True,
    # response_model=list[ButtonBase]
)
async def get_all_buttons(
        session: AsyncSession = Depends(get_async_session),
):
    all_buttons = await button_crud.get_multi(session)
    return all_buttons


@router.get(
    '/api/{button_id}',
    response_model=ButtonDatabase,
    response_model_exclude_none=True,
    # response_model=list[ButtonBase]
)
async def get_button_detail_by_id(
        button_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    button_detail = await button_crud.get(button_id, session)
    return button_detail


# test ok
@router.delete(
    '/api/{button_id}',
    response_model=ButtonDatabase,
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)]
)
async def delete_button(
    button_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """
    - Удалить кнопку.
    - **доступность:** Суперюзер.
    """
    button = await check_button_exists(
       button_id, session
    )
    for path_file in (
        *button.picture.replace(
            _STATIC_PICTURE_DIR, _STATIC_PICTURE_ROOT
        ).split(' ')[1:],
        *button.file.replace(_STATIC_DOC_DIR, _STATIC_DOC_ROOT).split(' ')[1:]
    ):
        if Path(path_file).exists():
            Path.unlink(Path(path_file))

    return await button_crud.remove(
        button, session
    )
