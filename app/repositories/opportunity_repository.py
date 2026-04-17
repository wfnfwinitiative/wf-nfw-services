import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, tuple_
from sqlalchemy.orm import aliased
from app.models.opportunity_models import Opportunity
from app.models.opportunity_event_models import OpportunityEvent
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

    async def _fetch_opportunities(self, driver_id: int | None = None):
        creator_user = aliased(User)
        driver_user = aliased(User)
        previous_status = aliased(Status)
        new_status = aliased(Status)

        latest_event_subq = (
            select(
                OpportunityEvent.opportunity_id,
                func.max(OpportunityEvent.opportunity_event_id).label("latest_event_id")
            )
            .group_by(OpportunityEvent.opportunity_id)
            .subquery()
        )

        stmt = (
            select(
                Opportunity.opportunity_id,
                Opportunity.donor_id,
                Opportunity.hunger_spot_id,
                Opportunity.status_id,
                Opportunity.driver_id,
                Opportunity.vehicle_id,
                Opportunity.creator_id,
                Opportunity.feeding_count,
                Opportunity.food_collected,
                Opportunity.estimated_count,
                Opportunity.estimated_unit,
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
                Donor.latitude.label('pickup_lat'),
                Donor.longitude.label('pickup_lng'),
                Status.status_name,
                driver_user.name.label('driver_name'),
                driver_user.mobile_number.label('driver_contact_no'),
                creator_user.name.label('creator_name'),
                Vehicle.vehicle_no.label('vehicle_name'),
                HungerSpot.spot_name.label('hunger_spot_name'),
                HungerSpot.location.label('drop_location'),
                HungerSpot.mobile_number.label('drop_location_contact_no'),
                HungerSpot.latitude.label('drop_lat'),
                HungerSpot.longitude.label('drop_lng'),
                previous_status.status_id.label("previous_status_id"),
                previous_status.status_name.label("previous_status_name"),
                new_status.status_id.label("new_status_id"),
                new_status.status_name.label("new_status_name"),
            )
            .join(Donor, Opportunity.donor_id == Donor.donor_id)
            .join(Status, Opportunity.status_id == Status.status_id)
            .join(creator_user, Opportunity.creator_id == creator_user.user_id)
            .outerjoin(driver_user, Opportunity.driver_id == driver_user.user_id)
            .outerjoin(Vehicle, Opportunity.vehicle_id == Vehicle.vehicle_id)
            .outerjoin(HungerSpot, Opportunity.hunger_spot_id == HungerSpot.hunger_spot_id)
            .outerjoin(latest_event_subq, Opportunity.opportunity_id == latest_event_subq.c.opportunity_id)
            .outerjoin(OpportunityEvent, OpportunityEvent.opportunity_event_id == latest_event_subq.c.latest_event_id)
            .outerjoin(previous_status, OpportunityEvent.previous_status_id == previous_status.status_id)
            .outerjoin(new_status, OpportunityEvent.new_status_id == new_status.status_id)
        )

        if driver_id is not None:
            stmt = stmt.where(Opportunity.driver_id == driver_id)

        result = await self.db.execute(stmt)

        opportunities = []
        for row in result:
            opportunities.append({
                'opportunity_id': row.opportunity_id,
                'opportunity_name': f"Opportunity {row.opportunity_id}",
                'donor_id': row.donor_id,
                'hunger_spot_id': row.hunger_spot_id,
                'donor_name': row.donor_name,
                'status_id': row.new_status_id,
                'status_name': row.new_status_name,
                'driver_id': row.driver_id,
                'driver_name': row.driver_name,
                'driver_contact_no': row.driver_contact_no,
                'vehicle_id': row.vehicle_id,
                'vehicle_name': row.vehicle_name,
                'creator_id': row.creator_id,
                'creator_name': row.creator_name,
                'estimated_count': row.estimated_count,
                'estimated_unit': row.estimated_unit,
                'feeding_count': row.feeding_count,
                'food_collected': float(row.food_collected) if row.food_collected is not None else None,
                'pickup_eta': row.pickup_eta,
                'delivery_by': row.delivery_by,
                'start_time': row.start_time,
                'end_time': row.end_time,
                'notes': row.notes,
                'image_link': row.image_link,
                'pickup_folder_id': row.pickup_folder_id,
                'delivery_folder_id': row.delivery_folder_id,
                'pickup_location': row.pickup_location,
                'pickup_contact_no': row.pickup_contact_no,
                'drop_location': row.drop_location,
                'drop_location_contact_no': row.drop_location_contact_no,
                'hunger_spot_name': row.hunger_spot_name,
                'pickup_lat': float(row.pickup_lat) if row.pickup_lat is not None else None,
                'pickup_lng': float(row.pickup_lng) if row.pickup_lng is not None else None,
                'drop_lat': float(row.drop_lat) if row.drop_lat is not None else None,
                'drop_lng': float(row.drop_lng) if row.drop_lng is not None else None,
                'created_at': row.created_at,
                'updated_at': row.updated_at,
                'previous_status_id': row.previous_status_id,
                'previous_status_name': row.previous_status_name,
                'new_status_id': row.new_status_id,
                'new_status_name': row.new_status_name,
            })
        return opportunities

    async def get_all(self):
        return await self._fetch_opportunities()

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
        return await self._fetch_opportunities(driver_id=driver_id)
