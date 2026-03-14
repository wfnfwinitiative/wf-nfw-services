from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.opportunity_allocation_models import OpportunityAllocation


class OpportunityAllocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = OpportunityAllocation(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_item(self, opportunity_item_id: int):
        result = await self.db.execute(
            select(OpportunityAllocation).where(
                OpportunityAllocation.opportunity_item_id == opportunity_item_id
            )
        )
        return result.scalars().all()

    async def delete(self, allocation_id: int):
        result = await self.db.execute(
            select(OpportunityAllocation).where(
                OpportunityAllocation.opportunity_allocation_id == allocation_id
            )
        )
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.flush()
            return True
        return False
