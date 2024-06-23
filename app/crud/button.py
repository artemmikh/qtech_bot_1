from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.button import Button


class CRUDButton(CRUDBase):
    async def create_with_pic(
            self,
            name: str,
            location: bool,
            department: bool,
            message: str,
            picture: str,
            session: AsyncSession,
    ):

        db_obj = self.model(name=name,
                            location=location,
                            department=department,
                            message=message,
                            picture=picture)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


button_crud = CRUDButton(Button)
