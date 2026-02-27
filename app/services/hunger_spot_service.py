from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.hunger_spot_repository import HungerSpotRepository
from app.models.hunger_spot_models import HungerSpot


class HungerSpotService:
    def __init__(self, db: AsyncSession):
        self.repository = HungerSpotRepository(db)
        self.db = db

    async def create_hunger_spot(self, creator_id: int = None, **data) -> HungerSpot:
        # creator_id is optional while auth is disabled
        spot = await self.repository.create(creator_id=creator_id, **data)
        await self.db.commit()
        return spot

    async def get_hunger_spot(self, hunger_spot_id: int) -> HungerSpot:
        spot = await self.repository.get_by_id(hunger_spot_id)
        if not spot:
            raise HTTPException(status_code=404, detail="Hunger spot not found")
        return spot

    async def get_all_hunger_spots(self) -> list[HungerSpot]:
        return await self.repository.get_all()

    async def update_hunger_spot(self, hunger_spot_id: int, **data) -> HungerSpot:
        spot = await self.repository.get_by_id(hunger_spot_id)
        if not spot:
            raise HTTPException(status_code=404, detail="Hunger spot not found")

        updated = await self.repository.update(hunger_spot_id, **data)
        await self.db.commit()
        return updated

    async def delete_hunger_spot(self, hunger_spot_id: int) -> dict:
        spot = await self.repository.get_by_id(hunger_spot_id)
        if not spot:
            raise HTTPException(status_code=404, detail="Hunger spot not found")

        await self.repository.delete(hunger_spot_id)
        await self.db.commit()
        return {"message": "Hunger spot deleted successfully"}