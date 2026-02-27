from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.vehicle_models import Vehicle


class VehicleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, creator_id: int, vehicle_no: str, notes: str = None):
        vehicle = Vehicle(
            creator_id=creator_id,
            vehicle_no=vehicle_no,
            notes=notes
        )
        self.db.add(vehicle)
        await self.db.flush()
        return vehicle

    async def get_by_id(self, vehicle_id: int):
        result = await self.db.execute(
            select(Vehicle).where(Vehicle.vehicle_id == vehicle_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(select(Vehicle))
        return result.scalars().all()

    async def delete(self, vehicle_id: int):
        vehicle = await self.get_by_id(vehicle_id)
        if vehicle:
            await self.db.delete(vehicle)
            await self.db.flush()
            return True
        return False