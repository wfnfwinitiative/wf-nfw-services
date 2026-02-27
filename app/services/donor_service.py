from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.donor_repository import DonorRepository
from app.models.donor_models import Donor


class DonorService:
    def __init__(self, db: AsyncSession):
        self.repository = DonorRepository(db)
        self.db = db

    async def create_donor(self, creator_id: int = None, **data) -> Donor:
        # creator_id is optional (will uncomment when column is added to DB)
        donor = await self.repository.create(creator_id=creator_id, **data)
        await self.db.commit()
        return donor

    async def get_donor(self, donor_id: int) -> Donor:
        donor = await self.repository.get_by_id(donor_id)
        if not donor:
            raise HTTPException(status_code=404, detail="Donor not found")
        return donor

    async def get_all_donors(self) -> list[Donor]:
        return await self.repository.get_all()

    async def update_donor(self, donor_id: int, **data) -> Donor:
        donor = await self.repository.get_by_id(donor_id)
        if not donor:
            raise HTTPException(status_code=404, detail="Donor not found")

        updated = await self.repository.update(donor_id, **data)
        await self.db.commit()
        return updated

    async def delete_donor(self, donor_id: int) -> dict:
        donor = await self.repository.get_by_id(donor_id)
        if not donor:
            raise HTTPException(status_code=404, detail="Donor not found")

        await self.repository.delete(donor_id)
        await self.db.commit()
        return {"message": "Donor deleted successfully"}