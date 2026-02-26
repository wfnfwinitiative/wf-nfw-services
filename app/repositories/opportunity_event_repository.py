from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.opportunity_event_models import OpportunityEvent


class OpportunityEventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = OpportunityEvent(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_opportunity(self, opportunity_id: int):
        result = await self.db.execute(
            select(OpportunityEvent).where(
                OpportunityEvent.opportunity_id == opportunity_id
            )
        )
        return result.scalars().all()