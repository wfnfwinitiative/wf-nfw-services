from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.opportunity_event_schema import (
    OpportunityEventCreate,
    OpportunityEventRead,
)
from app.services.opportunity_event_service import OpportunityEventService

router = APIRouter(prefix="/opportunity-events", tags=["Opportunity Events"])


@router.post("/", response_model=OpportunityEventRead)
async def create_event(
    payload: OpportunityEventCreate, db: AsyncSession = Depends(get_db)
):
    return await OpportunityEventService(db).create_event(**payload.dict())


@router.get(
    "/by-opportunity/{opportunity_id}", response_model=list[OpportunityEventRead]
)
async def get_events(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityEventService(db).get_events_for_opportunity(opportunity_id)
