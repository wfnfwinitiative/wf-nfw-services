from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.vehicle_models import Vehicle


class VehicleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, creator_id: int = None, vehicle_no: str = None, notes: str = None):
        params = {}
        if creator_id is not None:
            params["creator_id"] = creator_id
        if vehicle_no is not None:
            params["vehicle_no"] = vehicle_no
        if notes is not None:
            params["notes"] = notes
        vehicle = Vehicle(**params)
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

    async def update(self, vehicle_id: int, **kwargs):
        vehicle = await self.get_by_id(vehicle_id)
        if vehicle:
            for key, value in kwargs.items():
                setattr(vehicle, key, value)
            await self.db.flush()
        return vehicle