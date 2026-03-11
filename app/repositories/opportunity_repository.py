from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from sqlalchemy.orm import aliased
from app.models.opportunity_models import Opportunity
from app.models.donor_models import Donor
from app.models.status_models import Status
from app.models.user_models import User
from app.models.vehicle_models import Vehicle
from app.models.hunger_spot_models import HungerSpot


class OpportunityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = Opportunity(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_by_id(self, opportunity_id: int):
        result = await self.db.execute(
            select(Opportunity).where(
                Opportunity.opportunity_id == opportunity_id
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(select(Opportunity))
        return result.scalars().all()

    async def update(self, opportunity_id: int, **kwargs):
        obj = await self.get_by_id(opportunity_id)
        if obj:
            for k, v in kwargs.items():
                setattr(obj, k, v)
            await self.db.flush()
        return obj

    async def delete(self, opportunity_id: int):
        obj = await self.get_by_id(opportunity_id)
        if obj:
            await self.db.delete(obj)
            await self.db.flush()
            return True
        return False
    
    async def get_by_driver_id(self, driver_id: int):
        # Create aliases for the multiple User relationships
        creator_user = aliased(User)
        driver_user = aliased(User)
        
        result = await self.db.execute(
            select(
                Opportunity.opportunity_id,
                Opportunity.donor_id,
                Opportunity.status_id,
                Opportunity.driver_id,
                Opportunity.vehicle_id,
                Opportunity.creator_id,
                Opportunity.feeding_count,
                Opportunity.pickup_eta,
                Opportunity.delivery_by,
                Opportunity.start_time,
                Opportunity.end_time,
                Opportunity.notes,
                Opportunity.image_link,
                Opportunity.pickup_folder_id,
                Opportunity.delivery_folder_id,
                Opportunity.created_at,
                Opportunity.updated_at,
                Donor.donor_name,
                Donor.location.label('pickup_location'),
                Donor.mobile_number.label('pickup_contact_no'),
                Status.status_name,
                driver_user.name.label('driver_name'),
                creator_user.name.label('creator_name'),
                Vehicle.vehicle_no.label('vehicle_name'),
                HungerSpot.location.label('drop_location'),
                HungerSpot.mobile_number.label('drop_location_contact_no'),
            ).join(
                Donor, Opportunity.donor_id == Donor.donor_id
            ).join(
                Status, Opportunity.status_id == Status.status_id
            ).join(
                creator_user, Opportunity.creator_id == creator_user.user_id
            ).outerjoin(
                driver_user, Opportunity.driver_id == driver_user.user_id
            ).outerjoin(
                Vehicle, Opportunity.vehicle_id == Vehicle.vehicle_id
            ).outerjoin(
                HungerSpot, Opportunity.hunger_spot_id == HungerSpot.hunger_spot_id
            ).where(
                Opportunity.driver_id == driver_id
            )
        )
        
        # Convert rows to dictionaries that match OpportunityReadTest
        opportunities = []
        for row in result:
            opportunities.append({
                'opportunity_id': row.opportunity_id,
                'opportunity_name': f"Opportunity {row.opportunity_id}",
                'donor_id': row.donor_id,
                'donor_name': row.donor_name,
                'status_id': row.status_id,
                'status_name': row.status_name,
                'driver_id': row.driver_id,
                'driver_name': row.driver_name,
                'vehicle_id': row.vehicle_id,
                'vehicle_name': row.vehicle_name,
                'creator_id': row.creator_id,
                'creator_name': row.creator_name,
                'feeding_count': row.feeding_count,
                'pickup_eta': row.pickup_eta,
                'delivery_by': row.delivery_by,
                'start_time': row.start_time,
                'end_time': row.end_time,
                'notes': row.notes,
                'image_link': row.image_link,
                'pickup_location': row.pickup_location,
                'pickup_contact_no': row.pickup_contact_no,
                'drop_location': row.drop_location,
                'drop_location_contact_no': row.drop_location_contact_no,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
            })
        return opportunities