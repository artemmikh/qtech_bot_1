from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "12345678",  # Здесь указываем новый пароль
                "is_active": True,
                "is_superuser": False,
                "is_verified": False
            }
        }


class UserUpdate(schemas.BaseUserUpdate):
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "123456789",  # Пример нового пароля при обновлении
                "is_active": True,
                "is_superuser": False,
                "is_verified": False
            }
        }
