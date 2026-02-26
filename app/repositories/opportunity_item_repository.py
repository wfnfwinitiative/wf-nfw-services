from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.opportunity_item_models import OpportunityItem


class OpportunityItemRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = OpportunityItem(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_id(self, item_id: int):
        result = await self.db.execute(
            select(OpportunityItem).where(
                OpportunityItem.opportunity_item_id == item_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_opportunity(self, opportunity_id: int):
        result = await self.db.execute(
            select(OpportunityItem).where(
                OpportunityItem.opportunity_id == opportunity_id
            )
        )
        return result.scalars().all()

    async def delete(self, item_id: int):
        obj = await self.get_by_id(item_id)
        if obj:
            await self.db.delete(obj)
            await self.db.flush()
            return True
        return False