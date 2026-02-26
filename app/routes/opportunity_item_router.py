from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.opportunity_item_schemas import (
    OpportunityItemCreate,
    OpportunityItemRead,
    OpportunityItemUpdate,
)
from app.services.opportunity_item_service import OpportunityItemService

router = APIRouter(prefix="/opportunity-items", tags=["Opportunity Items"])


@router.post("/", response_model=OpportunityItemRead)
async def create_item(payload: OpportunityItemCreate, db: AsyncSession = Depends(get_db)):
    return await OpportunityItemService(db).create_item(**payload.dict())


@router.get("/{item_id}", response_model=OpportunityItemRead)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityItemService(db).get_item(item_id)


@router.get("/by-opportunity/{opportunity_id}", response_model=list[OpportunityItemRead])
async def get_items(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityItemService(db).get_items_for_opportunity(opportunity_id)


@router.patch("/{item_id}", response_model=OpportunityItemRead)
async def update_item(item_id: int, payload: OpportunityItemUpdate, db: AsyncSession = Depends(get_db)):
    return await OpportunityItemService(db).update_item(
        item_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityItemService(db).delete_item(item_id)