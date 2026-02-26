from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.vehicle_repository import VehicleRepository


class VehicleService:
    def __init__(self, db: AsyncSession):
        self.repo = VehicleRepository(db)
        self.db = db

    async def create_vehicle(self, creator_id: int, vehicle_no: str, notes: str = None):
        vehicle = await self.repo.create(creator_id, vehicle_no, notes)
        await self.db.commit()
        return vehicle

    async def get_vehicle(self, vehicle_id: int):
        vehicle = await self.repo.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    async def get_all_vehicles(self):
        return await self.repo.get_all()

    async def delete_vehicle(self, vehicle_id: int):
        if not await self.repo.delete(vehicle_id):
            raise HTTPException(status_code=404, detail="Vehicle not found")
        await self.db.commit()
        return {"message": "Vehicle deleted"}