import datetime as dt
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from rich.console import Console
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import fastapi_users
from app.crud.user import get_user
from app.models.user import User
from app.schemas.user import UserCreate, UserRead

console = Console()

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(settings.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(email: str, plain_password: str, session: AsyncSession) -> Optional[User]:
    user = await get_user(email, session)
    if not user:
        return None
    if not pwd_context.verify(plain_password, user.hashed_password):
        return None
    return user


async def decode_token(token: str, session: AsyncSession) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials."
    )
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception

    user = await get_user(email, session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_from_token(token: str = Depends(oauth2_scheme),
                                      session: AsyncSession = Depends(get_async_session)) -> User:
    user = await decode_token(token, session)
    return user


async def get_current_user_from_cookie(request: Request, session: AsyncSession = Depends(get_async_session)) -> User:
    token = request.cookies.get(settings.COOKIE_NAME)
    user = await decode_token(token, session)
    return user


@router.post("/token")
async def login_for_access_token(
        response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session)
) -> Dict[str, str]:
    user = await authenticate_user(form_data.email, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token = create_access_token(data={"email": user.email})

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=f"Bearer {access_token}",
        httponly=True
    )
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


@router.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse("login.html", context)


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request, session: AsyncSession = Depends(get_async_session)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            response = RedirectResponse("/", status.HTTP_302_FOUND)
            await login_for_access_token(response=response, form_data=form, session=session)
            form.__dict__.update(msg="Login Successful!")
            console.log("[green]Login successful!!!!")
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)


@router.get("/private", response_class=HTMLResponse)
async def private_page(request: Request, user: User = Depends(get_current_user_from_token)):
    context = {
        "user": user,
        "request": request
    }
    return templates.TemplateResponse("private.html", context)


@router.get("/auth/logout", response_class=RedirectResponse)
async def logout(request: Request):
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    return response
