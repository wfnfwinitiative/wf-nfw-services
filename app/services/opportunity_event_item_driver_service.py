from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.opportunity_event_repository import OpportunityEventRepository
from app.repositories.opportunity_item_repository import OpportunityItemRepository


class OpportunityEventItemDriverService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.event_repo = OpportunityEventRepository(db)
        self.item_repo = OpportunityItemRepository(db)

    async def process_opportunity(self, event_data, items_data):

        
        if not event_data or not isinstance(event_data, dict):
            raise ValueError("Valid opportunity event data is required")

       
        if not items_data or not isinstance(items_data, list):
            raise ValueError("At least one opportunity item is required")

        
        deduped_items = {}

        for item in items_data:
            name = item.get("food_name", "").strip().lower()
            if not name:
                raise ValueError("Food name cannot be empty")

            deduped_items[name] = item  # override old with latest

        items_data = list(deduped_items.values())

       
        async with self.db.begin():

            opportunity = await self.event_repo.create(event_data)

            created_items = []
            for item in items_data:
                item["opportunity_id"] = opportunity.opportunity_id
                created_items.append(await self.item_repo.create(item))

        return {
            "opportunity": opportunity,
            "items": created_items
        }