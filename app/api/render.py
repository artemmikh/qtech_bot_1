import os
from app.core.config import settings

from fastapi import APIRouter, Request, Form, UploadFile, Depends, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse
from app.core.config import settings

from app.core.db import get_async_session
from app.api.button import (create_button, get_all_buttons,
                            get_button_detail_by_id)

router = APIRouter(tags=['Render Bottons'])

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def render_all_buttons(request: Request,
                             session: AsyncSession = Depends(get_async_session)
                             ):
    context = await get_all_buttons(session)

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "context": context,
                                                     }
                                      )


@router.get("/create", response_class=HTMLResponse)
async def get_button_form(request: Request,
                          ):
    return templates.TemplateResponse("form.html", {"request": request,
                                                    }
                                      )


@router.post("/create")
async def post_button_form(name: str = Form(...),
                           is_moscow: bool = Form(...),
                           text: str = Form(...),
                           is_department: bool = Form(...),
                           is_active: bool = Form(...),
                           file_pic: list[UploadFile] = None,
                           file_doc: list[UploadFile] = None,
                           session: AsyncSession = Depends(get_async_session),
                           ):
    await create_button(name=name,
                        is_moscow=is_moscow,
                        text=text,
                        is_department=is_department,
                        is_active=is_active,
                        file_pic=file_pic,
                        file_doc=file_doc,
                        session=session
                        )
    return RedirectResponse(router.url_path_for('render_all_buttons'), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/{button_id}", response_class=HTMLResponse)
async def get_button_detail(request: Request,
                            button_id: int,
                            session: AsyncSession = Depends(get_async_session)
                            ):
    context = await get_button_detail_by_id(button_id, session)

    if context.picture:
        context.picture = context.picture.split(' ')

    if context.file:
        context.file = context.file.split(' ')

    return templates.TemplateResponse("button_detail.html",
                                      {"request": request,
                                       "context": context,
                                       }
                                      )


@router.get("/", response_class=HTMLResponse)
async def render_all_buttons(request: Request,
                             session: AsyncSession = Depends(get_async_session)
                             ):
    context = await get_all_buttons(session)

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "context": context,
                                                     }
                                      )


@router.get("/update/{button_id}", response_class=HTMLResponse)
async def update_button_form(request: Request,
                             button_id: int,
                             session: AsyncSession = Depends(get_async_session)
                             ):
    context = await get_button_detail_by_id(button_id, session)

    if context.picture:
        context.picture = context.picture.split(' ')


    if context.file:
        context.file = context.file.split(' ')


    return templates.TemplateResponse("form_patch.html", {"request": request,
                                                          "context": context,
                                                          'button_id': button_id
                                                          }
                                      )


@router.post("/update/{button_id}")
async def update_button_form(
        button_id: int,
        name: str = Form(...),
        is_moscow: bool = Form(...),
        text: str = Form(...),
        is_department: bool = Form(...),
        is_active: bool = Form(...),
        session: AsyncSession = Depends(get_async_session),
):
    button = await get_button_detail_by_id(button_id, session)
    button.name = name
    button.is_moscow = is_moscow
    button.text = text
    button.is_department = is_department
    button.is_active = is_active
    await session.commit()
    return RedirectResponse(router.url_path_for('get_button_detail', button_id=button_id),
                            status_code=status.HTTP_303_SEE_OTHER)


@router.post(
    '/delete_picture/{button_id}/{picture}',
)
async def del_button_picture(
        button_id: int,
        picture: str,
        session: AsyncSession = Depends(get_async_session),
):

    button = await get_button_detail_by_id(button_id, session)

    picture_list = button.picture.split(' ')

    new_pic_list = []
    for pic_url in picture_list:
        if picture not in pic_url:
            new_pic_list.append(pic_url)

    button.picture = ' '.join(new_pic_list)
    await session.commit()
    await session.refresh(button)

    current_working_directory = os.getcwd()
    delete_patch = current_working_directory + '/app/static/media/pics/' + picture
    os.remove(delete_patch)

    return RedirectResponse(router.url_path_for('update_button_form', button_id=button_id),
                            status_code=status.HTTP_303_SEE_OTHER)

@router.post(
    '/delete_file/{button_id}/{file}',
)
async def del_button_file(
        button_id: int,
        file: str,
        session: AsyncSession = Depends(get_async_session),
):
    button = await get_button_detail_by_id(button_id, session)

    file_list = button.file.split(' ')

    new_file_list = []
    for file_url in file_list:
        if file not in file_url:
            new_file_list.append(file_url)

    button.file = ' '.join(new_file_list)
    await session.commit()
    await session.refresh(button)

    current_working_directory = os.getcwd()
    delete_patch = current_working_directory + '/app/static/media/docs/' + file
    os.remove(delete_patch)

    return RedirectResponse(router.url_path_for('update_button_form', button_id=button_id),
                            status_code=status.HTTP_303_SEE_OTHER)