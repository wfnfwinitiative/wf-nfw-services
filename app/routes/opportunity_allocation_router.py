from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.opportunity_allocation_schemas import (
    OpportunityAllocationCreate,
    OpportunityAllocationRead,
    OpportunityAllocationUpdate,
)
from app.services.opportunity_allocation_service import OpportunityAllocationService

router = APIRouter(prefix="/opportunity-allocations", tags=["Opportunity Allocations"])


@router.post("/", response_model=OpportunityAllocationRead)
async def create_allocation(payload: OpportunityAllocationCreate, db: AsyncSession = Depends(get_db)):
    return await OpportunityAllocationService(db).create_allocation(**payload.dict())


@router.get("/{allocation_id}", response_model=OpportunityAllocationRead)
async def get_allocation(allocation_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityAllocationService(db).get_allocation(allocation_id)


@router.get("/by-item/{opportunity_item_id}", response_model=list[OpportunityAllocationRead])
async def get_allocations(opportunity_item_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityAllocationService(db).get_allocations_for_item(opportunity_item_id)


@router.patch("/{allocation_id}", response_model=OpportunityAllocationRead)
async def update_allocation(allocation_id: int, payload: OpportunityAllocationUpdate, db: AsyncSession = Depends(get_db)):
    return await OpportunityAllocationService(db).update_allocation(
        allocation_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{allocation_id}")
async def delete_allocation(allocation_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityAllocationService(db).delete_allocation(allocation_id)