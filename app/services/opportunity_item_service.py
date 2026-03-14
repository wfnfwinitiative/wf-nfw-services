from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_item_repository import OpportunityItemRepository


class OpportunityItemService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityItemRepository(db)
        self.db = db

    async def create_item(self, **data):
        obj = await self.repo.create(**data)
        await self.db.commit()
        return obj

    async def get_item(self, item_id: int):
        obj = await self.repo.get_by_id(item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        return obj

    async def get_items_for_opportunity(self, opportunity_id: int):
        return await self.repo.get_by_opportunity(opportunity_id)

    async def delete_item(self, item_id: int):
        if not await self.repo.delete(item_id):
            raise HTTPException(status_code=404, detail="Item not found")
        await self.db.commit()
        return {"message": "Item deleted"}
