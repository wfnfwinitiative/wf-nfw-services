from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.repositories.opportunity_repository import OpportunityRepository
from app.repositories.opportunity_item_repository import OpportunityItemRepository
from app.models.opportunity_event_models import OpportunityEvent


class OpportunityService:
    def __init__(self, db: AsyncSession):
        self.repo = OpportunityRepository(db)
        self.db = db

    async def create_opportunity(self, **data):
        obj = await self.repo.create(**data)
        # Create initial event recording the creation status
        event = OpportunityEvent(
            opportunity_id=obj.opportunity_id,
            previous_status_id=None,
            new_status_id=obj.status_id,
            creator_id=obj.creator_id,
            notes=obj.notes,
        )
        self.db.add(event)
        await self.db.commit()
        # Return as dict
        result = obj.__dict__.copy()
        result['previous_status_id'] = None
        result['new_status_id'] = obj.status_id
        # Ensure all fields are present
        result.setdefault('picked_up_at', None)
        result.setdefault('delivered_at', None)
        result.setdefault('pickup_folder_id', None)
        result.setdefault('delivery_folder_id', None)
        return result

    async def get_opportunity(self, opportunity_id: int):
        obj = await self.repo.get_by_id(opportunity_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        # Fetch opportunity items
        item_repo = OpportunityItemRepository(self.db)
        items = await item_repo.get_by_opportunity(opportunity_id)
        # Fetch latest event
        result = await self.db.execute(
            select(OpportunityEvent.previous_status_id, OpportunityEvent.new_status_id)
            .where(OpportunityEvent.opportunity_id == opportunity_id)
            .order_by(OpportunityEvent.opportunity_event_id.desc())
            .limit(1)
        )
        event = result.first()
        # Convert to dict and add items and status ids
        data = obj.__dict__.copy()
        data['opportunity_items'] = items
        if event:
            data['previous_status_id'] = event[0]
            data['new_status_id'] = event[1]
        else:
            data['previous_status_id'] = None
            data['new_status_id'] = None
        return data

    async def get_all_opportunities(self):
        return await self.repo.get_all()

    async def get_opportunities_by_driver_id(self, driver_id: int):
        return await self.repo.get_by_driver_id(driver_id)

    async def update_opportunity(self, opportunity_id: int, **data):
        creator_id = data.pop('creator_id', None)
        obj = await self.repo.get_by_id(opportunity_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Opportunity not found")

        # Determine the *effective* current status from the latest event,
        # because driver rejection only creates an event without updating status_id.
        latest_event_result = await self.db.execute(
            select(OpportunityEvent.new_status_id)
            .where(OpportunityEvent.opportunity_id == opportunity_id)
            .order_by(OpportunityEvent.opportunity_event_id.desc())
            .limit(1)
        )
        latest_new_status = latest_event_result.scalar_one_or_none()
        previous_status = latest_new_status if latest_new_status is not None else obj.status_id

        new_status = data.get('status_id')
        notes = data.get('notes')

        if new_status and new_status != previous_status:
            # Create event
            event = OpportunityEvent(
                opportunity_id=opportunity_id,
                previous_status_id=previous_status,
                new_status_id=new_status,
                creator_id=creator_id,
                notes=notes
            )
            self.db.add(event)

        # Update the obj
        for k, v in data.items():
            setattr(obj, k, v)

        await self.db.commit()

        # Return dict
        data = obj.__dict__.copy()
        data['previous_status_id'] = previous_status if new_status and new_status != previous_status else None
        data['new_status_id'] = new_status if new_status and new_status != previous_status else None
        # Ensure all fields are present
        data.setdefault('start_time', None)
        data.setdefault('end_time', None)
        data.setdefault('pickup_folder_id', None)
        data.setdefault('delivery_folder_id', None)
        return data

    async def delete_opportunity(self, opportunity_id: int):
        if not await self.repo.delete(opportunity_id):
            raise HTTPException(status_code=404, detail="Opportunity not found")
        await self.db.commit()
        return {"message": "Opportunity deleted"}