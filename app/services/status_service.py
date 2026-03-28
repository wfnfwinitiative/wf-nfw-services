from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.status_repository import StatusRepository


class StatusService:
    def __init__(self, db: AsyncSession):
        self.repo = StatusRepository(db)

    async def get_all_statuses(self):
        return await self.repo.get_all()