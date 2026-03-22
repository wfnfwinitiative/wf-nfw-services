from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased

from app.models.opportunity_models import Opportunity
from app.models.donor_models import Donor
from app.models.hunger_spot_models import HungerSpot
from app.models.status_models import Status
from app.models.user_models import User


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------- GRID DATA ----------------
    async def get_report_data(self, filters):
        driver_user = aliased(User)

        query = (
            select(
                Opportunity.opportunity_id,
                Opportunity.created_at,
                Opportunity.feeding_count,
                Opportunity.pickup_eta,
                Opportunity.delivery_by,

                Donor.donor_name,
                HungerSpot.spot_name.label("hunger_spot_name"),
                Status.status_name,
                driver_user.name.label("driver_name"),
            )
            .join(Donor, Opportunity.donor_id == Donor.donor_id)
            .outerjoin(HungerSpot, Opportunity.hunger_spot_id == HungerSpot.hunger_spot_id)
            .join(Status, Opportunity.status_id == Status.status_id)
            .outerjoin(driver_user, Opportunity.driver_id == driver_user.user_id)
        )

        conditions = []

        if filters.start_date:
            conditions.append(Opportunity.created_at >= filters.start_date)

        if filters.end_date:
            conditions.append(Opportunity.created_at <= filters.end_date)

        if filters.driver_id:
            conditions.append(Opportunity.driver_id == filters.driver_id)

        if filters.hunger_spot_id:
            conditions.append(Opportunity.hunger_spot_id == filters.hunger_spot_id)

        if filters.donor_id:
            conditions.append(Opportunity.donor_id == filters.donor_id)

        if filters.status_id:
            conditions.append(Opportunity.status_id == filters.status_id)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        rows = result.fetchall()

        return [
            {
                "opportunity_id": r.opportunity_id,
                "created_at": r.created_at,
                "feeding_count": r.feeding_count,
                "pickup_eta": r.pickup_eta,
                "delivery_by": r.delivery_by,
                "donor_name": r.donor_name,
                "hunger_spot_name": r.hunger_spot_name,
                "status_name": r.status_name,
                "driver_name": r.driver_name,
            }
            for r in rows
        ]

    # ---------------- GRAPH DATA ----------------
    async def get_graph_data(self, filters):
        query = select(
            func.date(Opportunity.created_at).label("date"),
            func.sum(Opportunity.feeding_count).label("total_feeding")
        )

        conditions = []

        if filters.start_date:
            conditions.append(Opportunity.created_at >= filters.start_date)

        if filters.end_date:
            conditions.append(Opportunity.created_at <= filters.end_date)

        if filters.driver_id:
            conditions.append(Opportunity.driver_id == filters.driver_id)

        if filters.hunger_spot_id:
            conditions.append(Opportunity.hunger_spot_id == filters.hunger_spot_id)

        if filters.status_id:
            conditions.append(Opportunity.status_id == filters.status_id)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.group_by(func.date(Opportunity.created_at)).order_by(func.date(Opportunity.created_at))

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
            func.sum(Opportunity.feeding_count).label("total_feeding"),
            func.count(Opportunity.opportunity_id).label("total_opportunities")
        )

        conditions = []

        if filters.start_date:
            conditions.append(Opportunity.created_at >= filters.start_date)

        if filters.end_date:
            conditions.append(Opportunity.created_at <= filters.end_date)

        if filters.driver_id:
            conditions.append(Opportunity.driver_id == filters.driver_id)

        if filters.hunger_spot_id:
            conditions.append(Opportunity.hunger_spot_id == filters.hunger_spot_id)

        if filters.status_id:
            conditions.append(Opportunity.status_id == filters.status_id)

        if conditions:
            query = query.where(and_(*conditions))

        result = await self.db.execute(query)
        row = result.first()

        return {
            "total_food": float(row.total_feeding or 0),
            "people_count": int(row.total_opportunities or 0)
        }