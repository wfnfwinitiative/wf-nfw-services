import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.opportunity_event_models import OpportunityEvent
from app.models.opportunity_models import Opportunity


class OpportunityEventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **data):
        obj = OpportunityEvent(**data)
        self.db.add(obj)
        await self.db.flush()

        new_status_id = data.get('new_status_id')
        opportunity_id = data.get('opportunity_id')

        if opportunity_id and new_status_id in (3, 5):
            opp_result = await self.db.execute(
                select(Opportunity).where(Opportunity.opportunity_id == opportunity_id)
            )
            opp = opp_result.scalar_one_or_none()
            if opp:
                now = datetime.datetime.now(tz=datetime.timezone.utc).replace(second=0, microsecond=0)
                if new_status_id == 3:
                    opp.picked_up_at = now
                elif new_status_id == 5:
                    opp.delivered_at = now
                await self.db.flush()

        return obj

    async def get_by_opportunity(self, opportunity_id: int):
        result = await self.db.execute(
            select(OpportunityEvent).where(
                OpportunityEvent.opportunity_id == opportunity_id
            )
        )
        return result.scalars().all()
    
    async def update(self, opportunity_event_id: int, **data):
        result = await self.db.execute(
            select(OpportunityEvent).where(
                OpportunityEvent.opportunity_event_id == opportunity_event_id
            )
        )
        obj = result.scalar_one_or_none()
        if not obj:
            return None
        for key, value in data.items():
            setattr(obj, key, value)
        await self.db.flush()
        return obj