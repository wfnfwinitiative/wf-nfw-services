from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_event_repository import OpportunityEventRepository


class OpportunityEventService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityEventRepository(db)
        self.db = db

    async def create_event(self, **data):
        obj = await self.repo.create(**data)
        await self.db.commit()
        return obj

    async def get_events_for_opportunity(self, opportunity_id: int):
        return await self.repo.get_by_opportunity(opportunity_id)
