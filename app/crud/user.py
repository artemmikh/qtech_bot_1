# crud/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User


class CRUDUser(CRUDBase):

    async def get_user_id_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> User:
        return (await session.execute(
            select(self.model.id).where(
                self.model.email == email
            )
        )).scalars().first()

    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession,
    ) -> User:
        return (await session.execute(
            select(self.model).where(
                self.model.email == email
            )
        )).scalars().first()


user_crud = CRUDUser(User)
