from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.driver_location_repository import DriverLocationRepository


class DriverLocationService:
    def __init__(self, db: AsyncSession):
        self.repo = DriverLocationRepository(db)
        self.db = db

    async def update_location(
        self,
        opportunity_id: int,
        driver_id: int,
        latitude: float,
        longitude: float,
        accuracy: float | None,
    ):
        row = await self.repo.upsert(opportunity_id, driver_id, latitude, longitude, accuracy)
        await self.db.commit()
        return row

    async def get_location(self, opportunity_id: int):
        row = await self.repo.get_by_opportunity(opportunity_id)
        if not row:
            raise HTTPException(
                status_code=404,
                detail="No location data available for this opportunity yet."
            )
        return row
