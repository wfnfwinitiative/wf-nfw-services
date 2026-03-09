from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.status_models import Status


class StatusRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_statuses(self):
        result = await self.db.execute(select(Status))
        return result.scalars().all()

    async def get_status(self, status_id: int):
        result = await self.db.execute(select(Status).where(Status.status_id == status_id))
        return result.scalar_one_or_none()

    async def create_status(self, status_name: str):
        status = Status(status_name=status_name)
        self.db.add(status)
        await self.db.commit()
        await self.db.refresh(status)
        return status

    async def update_status(self, status_id: int, status_name: str):
        status = await self.get_status(status_id)
        if not status:
            return None
        status.status_name = status_name
        await self.db.commit()
        await self.db.refresh(status)
        return status

    async def delete_status(self, status_id: int):
        status = await self.get_status(status_id)
        if not status:
            return None
        await self.db.delete(status)
        await self.db.commit()
        return status
