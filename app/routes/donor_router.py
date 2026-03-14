from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.donor_schemas import (
    DonorCreate,
    DonorRead,
    DonorUpdate,
)
from app.services.donor_service import DonorService
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/donors", tags=["Donors"])


@router.post("/", response_model=DonorRead)
async def create_donor(
    payload: DonorCreate,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR"])),
):
    return await DonorService(db).create_donor(
        creator_id=caller.get("user_id"),
        **payload.dict(),
    )


@router.get("/", response_model=list[DonorRead])
async def get_donors(db: AsyncSession = Depends(get_db)):
    return await DonorService(db).get_all_donors()


@router.get("/{donor_id}", response_model=DonorRead)
async def get_donor(donor_id: int, db: AsyncSession = Depends(get_db)):
    return await DonorService(db).get_donor(donor_id)


@router.patch(
    "/{donor_id}",
    response_model=DonorRead,
    dependencies=[Depends(require_roles(["ADMIN", "COORDINATOR"]))],
)
async def update_donor(
    donor_id: int,
    payload: DonorUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await DonorService(db).update_donor(
        donor_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete(
    "/{donor_id}", dependencies=[Depends(require_roles(["ADMIN", "COORDINATOR"]))]
)
async def delete_donor(
    donor_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await DonorService(db).delete_donor(donor_id)


@router.post(
    "/activate/{donor_id}",
    dependencies=[Depends(require_roles(["ADMIN", "COORDINATOR"]))],
)
async def activate_donor(
    donor_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await DonorService(db).activate_donor(donor_id)
