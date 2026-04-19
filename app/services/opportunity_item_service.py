from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_item_repository import OpportunityItemRepository
from app.repositories.opportunity_repository import OpportunityRepository


class OpportunityItemService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityItemRepository(db)
        self.opportunity_repo = OpportunityRepository(db)
        self.db = db

    async def _recalculate_feeding_count(self, opportunity_id: int):
        items = await self.repo.get_by_opportunity(opportunity_id)
        total = sum(float(item.quantity_value) for item in items)
        await self.opportunity_repo.update(opportunity_id, feeding_count=int(total * 2), food_collected=total)

    async def create_item(self, **data):
        obj = await self.repo.create(**data)
        await self._recalculate_feeding_count(obj.opportunity_id)
        await self.db.commit()
        return obj

    async def get_item(self, item_id: int):
        obj = await self.repo.get_by_id(item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        return obj

    async def get_items_for_opportunity(self, opportunity_id: int):
        return await self.repo.get_by_opportunity(opportunity_id)

    async def update_item(self, item_id: int, **data):
        obj = await self.repo.update(item_id, **data)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        await self._recalculate_feeding_count(obj.opportunity_id)
        await self.db.commit()
        return obj

    async def delete_item(self, item_id: int):
        obj = await self.repo.get_by_id(item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        opportunity_id = obj.opportunity_id
        await self.repo.delete(item_id)
        await self._recalculate_feeding_count(opportunity_id)
        await self.db.commit()
        return {"message": "Item deleted"}