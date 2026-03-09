from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.status_repository import StatusRepository


class StatusService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = StatusRepository(db)

    async def get_all_statuses(self):
        return await self.repo.get_all_statuses()

    async def get_status(self, status_id: int):
        return await self.repo.get_status(status_id)

    async def create_status(self, status_name: str):
        return await self.repo.create_status(status_name)

    async def update_status(self, status_id: int, status_name: str):
        return await self.repo.update_status(status_id, status_name)

    async def delete_status(self, status_id: int):
        return await self.repo.delete_status(status_id)
