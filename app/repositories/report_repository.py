from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased

from app.models.opportunity_models import Opportunity
from app.models.opportunity_event_models import OpportunityEvent
from app.models.donor_models import Donor
from app.models.hunger_spot_models import HungerSpot
from app.models.status_models import Status
from app.models.user_models import User
from app.models.vehicle_models import Vehicle


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------- COMMON FILTER ----------------
    def apply_filters(self, conditions, filters):
        if filters.start_date:
            conditions.append(Opportunity.created_at >= filters.start_date)

        if filters.end_date:
            conditions.append(Opportunity.created_at <= filters.end_date)

        if filters.driver_ids:
            conditions.append(Opportunity.driver_id.in_(filters.driver_ids))

        if filters.hunger_spot_ids:
            conditions.append(Opportunity.hunger_spot_id.in_(filters.hunger_spot_ids))

        if filters.vehicle_ids:
            conditions.append(Opportunity.vehicle_id.in_(filters.vehicle_ids))

        if filters.donor_ids:
            conditions.append(Opportunity.donor_id.in_(filters.donor_ids))

        if filters.status_ids:
            latest_status_subq = (
                select(OpportunityEvent.new_status_id)
                .where(OpportunityEvent.opportunity_id == Opportunity.opportunity_id)
                .order_by(OpportunityEvent.opportunity_event_id.desc())
                .limit(1)
                .scalar_subquery()
            )
            conditions.append(latest_status_subq.in_(filters.status_ids))

        return conditions

    # ---------------- GRID ----------------
    async def get_report_data(self, filters):
        driver_user = aliased(User)
        event_status = aliased(Status)

        # Subquery: latest event id per opportunity
        latest_event_subq = (
            select(
                OpportunityEvent.opportunity_id,
                func.max(OpportunityEvent.opportunity_event_id).label("latest_event_id"),
            )
            .group_by(OpportunityEvent.opportunity_id)
            .subquery()
        )
        latest_event = aliased(OpportunityEvent)

        query = (
            select(
                Opportunity.opportunity_id,
                Opportunity.created_at,
                Opportunity.feeding_count,
                Opportunity.food_collected,
                Opportunity.pickup_eta,
                Opportunity.delivery_by,

                Donor.donor_name,
                HungerSpot.spot_name.label("hunger_spot_name"),
                event_status.status_name,
                driver_user.name.label("driver_name"),
                Vehicle.vehicle_no,
            )
            .join(Donor, Opportunity.donor_id == Donor.donor_id)
            .outerjoin(HungerSpot, Opportunity.hunger_spot_id == HungerSpot.hunger_spot_id)
            .outerjoin(latest_event_subq, Opportunity.opportunity_id == latest_event_subq.c.opportunity_id)
            .outerjoin(latest_event, latest_event.opportunity_event_id == latest_event_subq.c.latest_event_id)
            .outerjoin(event_status, latest_event.new_status_id == event_status.status_id)
            .outerjoin(driver_user, Opportunity.driver_id == driver_user.user_id)
            .outerjoin(Vehicle, Opportunity.vehicle_id == Vehicle.vehicle_id)
        )

        conditions = self.apply_filters([], filters)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        rows = result.fetchall()

        return [
            {
                "opportunity_id": r.opportunity_id,
                "created_at": r.created_at,
                "feeding_count": r.feeding_count,
                "food_collected": r.food_collected,
                "pickup_eta": r.pickup_eta,
                "delivery_by": r.delivery_by,
                "donor_name": r.donor_name,
                "hunger_spot_name": r.hunger_spot_name,
                "status_name": r.status_name,
                "driver_name": r.driver_name,
                "vehicle_no": r.vehicle_no,
            }
            for r in rows
        ]

    # ---------------- GRAPH ----------------
    async def get_graph_data(self, filters):
        query = select(
            func.date(Opportunity.created_at).label("date"),
            func.sum(Opportunity.feeding_count).label("total_feeding")
        )

        conditions = self.apply_filters([], filters)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.group_by(func.date(Opportunity.created_at)) \
                     .order_by(func.date(Opportunity.created_at))

        result = await self.db.execute(query)

        return [
            {
                "date": str(r.date),
                "feeding_count": float(r.total_feeding or 0)
            }
            for r in result
        ]

    # ---------------- SUMMARY ----------------
    async def get_summary(self, filters):
     query = select(
        func.sum(Opportunity.food_collected).label("total_food"),
        func.count(Opportunity.opportunity_id).label("total_opportunities"),
        func.sum(Opportunity.feeding_count).label("total_people_fed")
    )

     conditions = self.apply_filters([], filters)

     if conditions:
        query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        row = result.mappings().first()   # ✅ FIX

        return {
            "total_food": float(row["total_food"] or 0),
            "opportunity_count": int(row["total_opportunities"] or 0),
            "people_fed": float(row["total_people_fed"] or 0)
        }