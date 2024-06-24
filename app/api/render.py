from fastapi import APIRouter, Request, Form, UploadFile, Depends, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from app.core.db import get_async_session
from app.api.button import create_button, get_all_buttons


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
                           location: bool = Form(...),
                           department: bool = Form(...),
                           message: str = Form(...),
                           file: UploadFile = None,
                           session: AsyncSession = Depends(get_async_session),
                           ):
    await create_button(name=name,
                        location=location,
                        department=department,
                        message=message,
                        file=file,
                        session=session
                        )
    return RedirectResponse(router.url_path_for('render_all_buttons'), status_code=status.HTTP_303_SEE_OTHER)



