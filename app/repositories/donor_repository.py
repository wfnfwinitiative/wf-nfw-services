from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.donor_models import Donor


class DonorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        creator_id: int = None,
        donor_name: str = None,
        city: str = None,
        pincode: str = None,
        contact_person: str = None,
        mobile_number: str = None,
        address: str = None,
        location: str = None,
        latitude: float = None,
        longitude: float = None,
        is_active: bool = True
    ) -> Donor:
        donor = Donor(
            creator_id=creator_id,
            donor_name=donor_name,
            city=city,
            pincode=pincode,
            contact_person=contact_person,
            mobile_number=mobile_number,
            address=address,
            location=location,
            latitude=latitude,
            longitude=longitude,
            is_active=is_active,
        )
        self.db.add(donor)
        await self.db.flush()
        return donor

    async def get_by_id(self, donor_id: int) -> Donor:
        result = await self.db.execute(
            select(Donor).where(Donor.donor_id == donor_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Donor]:
        result = await self.db.execute(select(Donor))
        return result.scalars().all()

    async def update(self, donor_id: int, **kwargs) -> Donor:
        donor = await self.get_by_id(donor_id)
        if donor:
            for key, value in kwargs.items():
                setattr(donor, key, value)
            await self.db.flush()
        return donor

    async def delete(self, donor_id: int) -> bool:
        donor = await self.get_by_id(donor_id)
        if donor:
            await self.db.delete(donor)
            await self.db.flush()
            return True
        return False