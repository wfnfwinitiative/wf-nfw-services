from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.opportunity_models import Opportunity


class OpportunityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = Opportunity(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_id(self, opportunity_id: int):
        result = await self.db.execute(
            select(Opportunity).where(
                Opportunity.opportunity_id == opportunity_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(select(Opportunity))
        return result.scalars().all()

    async def update(self, opportunity_id: int, **kwargs):
        obj = await self.get_by_id(opportunity_id)
        if obj:
            for k, v in kwargs.items():
                setattr(obj, k, v)
            await self.db.flush()
        return obj

    async def delete(self, opportunity_id: int):
        obj = await self.get_by_id(opportunity_id)
        if obj:
            await self.db.delete(obj)
            await self.db.flush()
            return True
        return False