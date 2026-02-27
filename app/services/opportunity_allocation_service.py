from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_allocation_repository import OpportunityAllocationRepository


class OpportunityAllocationService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityAllocationRepository(db)
        self.db = db

    async def create_allocation(self, **data):
        obj = await self.repo.create(**data)
        await self.db.commit()
        return obj

    async def get_allocations_for_item(self, opportunity_item_id: int):
        return await self.repo.get_by_item(opportunity_item_id)

    async def delete_allocation(self, allocation_id: int):
        if not await self.repo.delete(allocation_id):
            raise HTTPException(status_code=404, detail="Allocation not found")
        await self.db.commit()
        return {"message": "Allocation deleted"}