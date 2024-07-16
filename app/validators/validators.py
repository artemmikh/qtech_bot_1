from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.button import Button
from app.models.user import User
from app.crud.button import button_crud
from app.crud.user import user_crud


async def check_buttons_name_duplicate(
    button_name: str,
    session: AsyncSession,
    button_id: Optional[int] = None
) -> None:
    """Валидация названия кнопки на наличие дубликатов."""
    db_button_id = (
        await button_crud.get_buttons_id_by_name(
            button_name=button_name,
            session=session
        )
    )
    if (button_id and db_button_id and (
        button_id != db_button_id
    )) or (db_button_id and not button_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Кнопка с таким именем уже существует.'
        )


# test ok
async def check_button_exists(
    button_id: int,
    session: AsyncSession,
) -> Button:
    db_button_id = await button_crud.get(
        obj_id=button_id, session=session
    )
    if not db_button_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Кнопка не найденаю'
        )
    return db_button_id


async def check_user_username_duplicate(
    email: str,
    session: AsyncSession,
) -> None:
    """Валидация имени пользователя на наличие дубликатов."""
    user_id = await user_crud.get_user_id_by_email(
        email=email, session=session
    )
    if user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пользователь с таким email уже существует.'
        )


async def check_user_exists(
    email: str,
    session: AsyncSession,
) -> User:
    user = await user_crud.get_user_by_email(
        email=email, session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Пользователь с таким username не найден.'
        )
    return user
