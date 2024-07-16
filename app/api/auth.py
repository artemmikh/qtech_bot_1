import aiohttp

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.core.config import URL_DOMAIN
from app.core.init_db import create_user
from app.crud.user import user_crud
from app.schemas.user import RegistrationForm, RemoveForm, UserCreate
from app.validators.validators import (
     check_user_exists, check_user_username_duplicate
)


router = APIRouter(tags=['auth [Form]'])
templates = Jinja2Templates(directory='app/templates/auth')


@router.get(
    '/auth/register/form',
    # dependencies=[Depends(current_superuser)],
    response_class=HTMLResponse
)
async def user_registration_(request: Request):
    """
    Отображение формы Авторизация / регистрация нового пользователя.
    """
    return templates.TemplateResponse(
        'register.html', context={"request": request}
    )


@router.post(
    '/auth/register/form',
    response_class=HTMLResponse
)
async def user_registration(
    request: Request,
    credentials: RegistrationForm = Depends(RegistrationForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Авторизация / регистрация нового пользователя.
    """
    await check_user_username_duplicate(
        email=credentials.email, session=session
    )
    async with aiohttp.ClientSession() as aiohttp_session:
        async with aiohttp_session.post(
            f'{URL_DOMAIN}/auth/register',
            json=UserCreate(
                email=credentials.email,
                password=credentials.password,
                is_active=True,
                is_superuser=False,
                is_verified=False
            ).dict(),
            headers={'Content-Type': 'application/json'}
        ) as response:
            user = await response.json()

    return templates.TemplateResponse(
        'success.html',
        context={
            'request': request,
            'message': f'Пользователь [{user.get("email")}] зарегистрирован.',
            'redirect_message': (
                'Вы хотите зарегистрировать еще одного пользователя?'
            ),
            'redirect_to': '/auth/register/form',
            'redirect_button': 'Регистрация.'
        }
    )


@router.get(
    '/auth/register/superuser/form',
    # dependencies=[Depends(current_superuser)],
    response_class=HTMLResponse
)
async def superuser_registration_(request: Request):
    """
    Отображение Формы авторизации / регистрации нового администратора.
    """
    return templates.TemplateResponse(
        'superuser_registration.html',
        context={"request": request}
    )


@router.post(
    '/auth/register/superuser/form',
    response_class=HTMLResponse,
    # dependencies=[Depends(current_superuser)],
)
async def superuser_registration(
    request: Request,
    credentials: RegistrationForm = Depends(RegistrationForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Авторизация / регистрация нового администратора.
    """
    await check_user_username_duplicate(
        email=credentials.email, session=session
    )
    await create_user(
            email=credentials.email,
            password=credentials.password,
            is_superuser=True,
        )
    user = await user_crud.get_user_by_email(
        email=credentials.email, session=session
    )
    return templates.TemplateResponse(
        'success.html',
        context={
            'request': request,
            'message': f'Администратор [{user.email}] зарегистрирован.',
            'redirect_message': (
                'Вы хотите зарегистрировать еще одного администратора?'
            ),
            'redirect_to': '/auth/register/superuser/form',
            'redirect_button': 'Регистрация.'
        }
    )


@router.get(
    '/auth/register/delete/form',
    # dependencies=[Depends(current_superuser)],
    response_class=HTMLResponse
)
async def delete_user_(request: Request):
    """
    Отображение формы удаления администратора.
    """
    return templates.TemplateResponse(
        'delete_user.html', context={"request": request}
    )


@router.post(
    '/auth/register/delete/form',
    response_class=HTMLResponse,
    # dependencies=[Depends(current_superuser)],
)
async def delete_user(
    request: Request,
    credentials: RemoveForm = Depends(RemoveForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить администратора по имени пользователя(email).
    """
    user_db = await check_user_exists(
        email=credentials.email, session=session
    )
    await user_crud.remove(
        db_obj=user_db, session=session
    )
    return templates.TemplateResponse(
        'success.html',
        context={
            'request': request,
            'message': f'Пользователь [{credentials.email}] удален.',
            'redirect_message': (
                'Вы хотите зарегистрировать нового пользователя?'
            ),
            'redirect_to': '/auth/register/form',
            'redirect_button': 'Регистрация.'
        }
    )


@router.get(
    '/auth/register/superuser/delete/form',
    # dependencies=[Depends(current_superuser)],
    response_class=HTMLResponse
)
async def delete_superuser_(request: Request):
    """
    Отображение формы удаления администратора.
    """
    return templates.TemplateResponse(
        'delete_superuser.html', context={"request": request}
    )


@router.post(
    '/auth/register/superuser/delete/form',
    response_class=HTMLResponse,
    # dependencies=[Depends(current_superuser)],
)
async def delete_superuser(
    request: Request,
    credentials: RemoveForm = Depends(RemoveForm.as_form),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Удалить администратора по имени пользователя(email).
    """
    user_db = await check_user_exists(
        email=credentials.email, session=session
    )
    await user_crud.remove(
        db_obj=user_db, session=session
    )
    return templates.TemplateResponse(
        'success.html',
        context={
            'request': request,
            'message': f'Администратор [{credentials.email}] удален.',
            'redirect_message': (
                'Вы хотите зарегистрировать администратора?'
            ),
            'redirect_to': '/auth/register/superuser/form',
            'redirect_button': 'Регистрация.'
        }
    )
