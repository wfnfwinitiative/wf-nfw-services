from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.opportunity_schemas import (
    OpportunityCreate,
    OpportunityDetailedRead,
    OpportunityRead,
    OpportunityUpdate,
    OpportunityDetailRead,
)
from app.services.opportunity_service import OpportunityService
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.post("/", response_model=OpportunityRead)
async def create_opportunity(
    payload: OpportunityCreate,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR"])),
):
    return await OpportunityService(db).create_opportunity(
        creator_id=caller.get("user_id"),
        **payload.dict(),
    )


@router.get("/", response_model=list[OpportunityDetailedRead])
async def get_opportunities(db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).get_all_opportunities()


@router.get("/{opportunity_id}", response_model=OpportunityDetailRead)
async def get_opportunity(opportunity_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).get_opportunity(opportunity_id)


@router.get("/driver/{driver_id}", response_model=list[OpportunityDetailedRead])
async def get_opportunities_by_driver_id(driver_id: int, db: AsyncSession = Depends(get_db)):
    return await OpportunityService(db).get_opportunities_by_driver_id(driver_id)


@router.patch("/{opportunity_id}", response_model=OpportunityRead, dependencies=[Depends(require_roles(["ADMIN", "COORDINATOR"]))])
async def update_opportunity(
        opportunity_id: int,
        payload: OpportunityUpdate,
        db: AsyncSession = Depends(get_db),
        caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR"])),
):
    data = payload.dict(exclude_unset=True)
    data['creator_id'] = caller.get("user_id")
    return await OpportunityService(db).update_opportunity(opportunity_id, **data)

