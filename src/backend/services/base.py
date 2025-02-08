from fastapi.encoders import jsonable_encoder
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
