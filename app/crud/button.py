import select
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.button import Button
from app.schemas.button import ButtonUpdate


class CRUDButton(CRUDBase):
    async def create_with_pic(
            self,
            name: str,
            is_moscow: bool,
            text: str,
            picture: str,
            file: str,
            is_department: bool,
            is_active: bool,
            session: AsyncSession,
    ):

        db_obj = self.model(name=name,
                            is_moscow=is_moscow,
                            text=text,
                            picture=picture,
                            file=file,
                            is_department=is_department,
                            is_active=is_active
                            )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_button_by_id(
        button_id: int,
        session: AsyncSession,
    ):
        db_button = await session.execute(select(Button).where(Button.id == button_id))
        db_button = db_button.scalars().first()
        return db_button

    async def update_button(
        db_button: Button,
        button_in: ButtonUpdate,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_button)
        update_data = button_in.dict(exclude_unset=True, exclude_none=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_button, field, update_data[field])
        session.add(db_button)
        await session.commit()
        await session.refresh(db_button)
        return db_button


button_crud = CRUDButton(Button)
