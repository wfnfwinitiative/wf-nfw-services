from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
        """Insert or update the single live-location row for this opportunity."""
        result = await self.db.execute(
            select(DriverLocation).where(DriverLocation.opportunity_id == opportunity_id)
        )
        row = result.scalar_one_or_none()

        if row:
            row.driver_id = driver_id
            row.latitude = latitude
            row.longitude = longitude
            row.accuracy = accuracy
        else:
            row = DriverLocation(
                opportunity_id=opportunity_id,
                driver_id=driver_id,
                latitude=latitude,
                longitude=longitude,
                accuracy=accuracy,
            )
            self.db.add(row)

        await self.db.flush()
        return row

    async def get_by_opportunity(self, opportunity_id: int) -> DriverLocation | None:
        result = await self.db.execute(
            select(DriverLocation).where(DriverLocation.opportunity_id == opportunity_id)
        )
        return result.scalar_one_or_none()
