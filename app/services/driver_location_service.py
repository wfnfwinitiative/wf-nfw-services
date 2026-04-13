from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.driver_location_repository import DriverLocationRepository
from app.repositories.opportunity_repository import OpportunityRepository


class DriverLocationService:
    def __init__(self, db: AsyncSession):
        self.repo = DriverLocationRepository(db)
        self.opp_repo = OpportunityRepository(db)
        self.db = db

    async def update_location(
        self,
        opportunity_id: int,
        driver_id: int,
        latitude: float,
        longitude: float,
        accuracy: float | None,
    ):
        opp = await self.opp_repo.get_by_id(opportunity_id)
        if not opp:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        if opp.driver_id != driver_id:
            raise HTTPException(
                status_code=403,
                detail="You are not the assigned driver for this opportunity",
            )
        result = await self.repo.upsert(
            opportunity_id=opportunity_id,
            driver_id=driver_id,
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
        )
        await self.db.commit()
        return result

    async def get_location(self, opportunity_id: int):
        loc = await self.repo.get_by_opportunity(opportunity_id)
        if not loc:
            raise HTTPException(
                status_code=404,
                detail="No location data available for this opportunity",
            )
        return loc
