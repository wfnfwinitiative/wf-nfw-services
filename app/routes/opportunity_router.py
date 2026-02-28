from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.opportunity_schemas import (
    OpportunityCreate,
    OpportunityRead,
    OpportunityUpdate,
)
from app.services.opportunity_service import OpportunityService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.post("/", response_model=OpportunityRead)
async def create_opportunity(
    payload: OpportunityCreate,
    db: AsyncSession = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    return await OpportunityService(db).create_opportunity(
        creator_id=4,
        **payload.dict(),
    )


@router.get("/", response_model=list[OpportunityRead])
async def get_opportunities(db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).get_all_opportunities()


@router.get("/{opportunity_id}", response_model=OpportunityRead)
async def get_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).get_opportunity(opportunity_id)


@router.patch("/{opportunity_id}", response_model=OpportunityRead)
async def update_opportunity(opportunity_id: int, payload: OpportunityUpdate, db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).update_opportunity(
        opportunity_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{opportunity_id}")
async def delete_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).delete_opportunity(opportunity_id)