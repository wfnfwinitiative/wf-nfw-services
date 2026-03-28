from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.hunger_spot_models import HungerSpot


class HungerSpotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        creator_id: int = None,
        spot_name: str = None,
        city: str = None,
        pincode: str = None,
        contact_person: str = None,
        mobile_number: str = None,
        address: str = None,
        location: str = None,
        latitude: float = None,
        longitude: float = None,
        capacity_meals: int = None,
        is_active: bool = True
    ) -> HungerSpot:
        params = {
            "spot_name": spot_name,
            "city": city,
            "pincode": pincode,
            "contact_person": contact_person,
            "mobile_number": mobile_number,
            "address": address,
            "location": location,
            "latitude": latitude,
            "longitude": longitude,
            "capacity_meals": capacity_meals,
            "is_active": is_active,
        }
        if creator_id is not None:
            params["creator_id"] = creator_id
        spot = HungerSpot(**{k: v for k, v in params.items() if v is not None})
        self.db.add(spot)
        await self.db.flush()
        return spot

    async def get_by_id(self, hunger_spot_id: int) -> HungerSpot:
        result = await self.db.execute(
            select(HungerSpot).where(HungerSpot.hunger_spot_id == hunger_spot_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[HungerSpot]:
        result = await self.db.execute(select(HungerSpot))
        return result.scalars().all()

    async def update(self, hunger_spot_id: int, **kwargs) -> HungerSpot:
        spot = await self.get_by_id(hunger_spot_id)
        if spot:
            for key, value in kwargs.items():
                setattr(spot, key, value)
            await self.db.flush()
        return spot

    async def delete(self, hunger_spot_id: int) -> bool:
        spot = await self.get_by_id(hunger_spot_id)
        if spot:
            await self.db.delete(spot)
            await self.db.flush()
            return True
        return False