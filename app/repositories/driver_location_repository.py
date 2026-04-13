from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from app.models.driver_location_models import DriverLocation


class DriverLocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert(
        self,
        opportunity_id: int,
        driver_id: int,
        latitude: float,
        longitude: float,
        accuracy: float | None,
    ) -> DriverLocation:
        existing = await self.get_by_opportunity(opportunity_id)
        if existing:
            existing.latitude = latitude
            existing.longitude = longitude
            existing.accuracy = accuracy
            existing.updated_at = func.now()
            await self.db.flush()
            return existing

        obj = DriverLocation(
            opportunity_id=opportunity_id,
            driver_id=driver_id,
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_opportunity(self, opportunity_id: int) -> DriverLocation | None:
        result = await self.db.execute(
            select(DriverLocation).where(
                DriverLocation.opportunity_id == opportunity_id
            )
        )
        return result.scalar_one_or_none()
