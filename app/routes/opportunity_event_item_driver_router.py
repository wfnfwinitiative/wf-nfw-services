from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.opportunity_event_item_driver_schemas import (
    OpportunityEventItemDriverCreate,
    OpportunityEventItemDriverRead,
)

from app.services.opportunity_event_item_driver_service import (
    OpportunityEventItemDriverService,
)


router = APIRouter(
    prefix="/opportunity-event-items-driver",
    tags=["Opportunity Event Item Driver"],
)


@router.post("/", response_model=OpportunityEventItemDriverRead)
async def create_opportunity_event_items(
    payload: OpportunityEventItemDriverCreate,
    db: AsyncSession = Depends(get_db),
):
    return await OpportunityEventItemDriverService(db).process_opportunity(
        **payload.model_dump()
    )