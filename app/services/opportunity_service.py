from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_repository import OpportunityRepository


class OpportunityService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityRepository(db)
        self.db = db

    async def create_opportunity(self, **data):
        obj = await self.repo.create(**data)
        await self.db.commit()
        return obj

    async def get_opportunity(self, opportunity_id: int):
        obj = await self.repo.get_by_id(opportunity_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        return obj

    async def get_all_opportunities(self):
        return await self.repo.get_all()

    async def get_opportunities_by_driver_id(self, driver_id: int):
        return await self.repo.get_by_driver_id(driver_id)

    async def update_opportunity(self, opportunity_id: int, **data):
        obj = await self.repo.update(opportunity_id, **data)
        if not obj:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        await self.db.commit()
        return obj

    async def delete_opportunity(self, opportunity_id: int):
        if not await self.repo.delete(opportunity_id):
            raise HTTPException(status_code=404, detail="Opportunity not found")
        await self.db.commit()
        return {"message": "Opportunity deleted"}
