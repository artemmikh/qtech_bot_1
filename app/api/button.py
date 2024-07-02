import os
from pathlib import Path
import uuid
import shutil
from typing import Annotated, List

from fastapi import (
    APIRouter, Depends, UploadFile, File, Form
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.button import ButtonDatabase
from app.core.db import get_async_session
from app.core.config import (
    _STATIC_PICTURE_DIR, _STATIC_DOC_DIR, _STATIC_PICTURE_ROOT,
    _STATIC_DOC_ROOT
)
from app.crud.button import button_crud
from app.models.button import Button
from app.validators.validators import (
    check_buttons_name_duplicate, check_button_exists
)

router = APIRouter(
    tags=['API Bottons']
)


"""
Рефакторинг кода:
test=ok
Отимизирация кода, изменение формирования имени файла для исключения
повтора и конфликтов.
"""


@router.post(
    '/api/create',
    response_model=ButtonDatabase,
    response_model_exclude_none=True,
)
async def create_button(
        name: Annotated[str, Form()],
        is_moscow: Annotated[bool, Form()],
        text: Annotated[str, Form()],
        is_department: Annotated[bool, Form()],
        is_active: Annotated[bool, Form()],
        file_pic: List[UploadFile] = File(...),
        file_doc: List[UploadFile] = File(...),
        session: AsyncSession = Depends(get_async_session),
):
    """
    - Создать кнопку.
    - **доступность:** Суперюзер.
    """
    Path(_STATIC_PICTURE_ROOT).mkdir(parents=True, exist_ok=True)
    Path(_STATIC_DOC_ROOT).mkdir(parents=True, exist_ok=True)
    pictures, files = '', ''
    for file in (*file_pic, *file_doc):
        path_root_button = _STATIC_PICTURE_ROOT if (
            file in file_pic
        ) else _STATIC_DOC_ROOT
        if file.filename:
            filename = str(uuid.uuid4()) + str(file.filename)
            with open(os.path.join(path_root_button, filename), 'wb') as item:
                shutil.copyfileobj(file.file, item)
            if file in file_pic:
                pictures += ' ' + _STATIC_PICTURE_DIR + filename
            if file in file_doc:
                files += ' ' + _STATIC_DOC_DIR + filename

    return await button_crud.create_with_pic(
        name=name,
        is_moscow=is_moscow,
        text=text,
        picture=pictures,
        file=files,
        is_department=is_department,
        is_active=is_active,
        session=session
    )


@router.get(
    '/api',
    response_model=list[ButtonDatabase],
    response_model_exclude_none=True,
)
async def get_all_buttons(
        session: AsyncSession = Depends(get_async_session),
):
    all_buttons = await button_crud.get_multi(session)
    return all_buttons


# test ok
@router.get(
    '/api/{button_id}',
    response_model=ButtonDatabase,
    response_model_exclude_none=True,
)
async def get_button_detail_by_id(
        button_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> Button:
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
