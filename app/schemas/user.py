# app/schemas/user.py
from fastapi import Form
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class RemoveForm(BaseModel):
    email: EmailStr

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
    ):
        return cls(email=email)


class RegistrationForm(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...),
    ):
        return cls(
            email=email,
            password=password,
        )
