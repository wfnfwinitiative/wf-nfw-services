from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.status_models import Status


class StatusRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Status))
        return result.scalars().all()