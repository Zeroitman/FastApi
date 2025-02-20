from typing import Set
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ServiceBase:
    def __init__(self, model):
        self.model = model

    async def create(self, db: AsyncSession, commit: bool = True, *, obj_in):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        if commit:
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        else:
            return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            exclude_fields: Set[str] = {},
            db_obj,
            obj_in
    ):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(
                exclude_unset=True,
                exclude=exclude_fields,
            )
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> None:
        result = await db.scalars(
            select(self.model).where(self.model.id == id)
        )
        obj = result.first()
        await db.delete(obj)
        await db.commit()
        return
