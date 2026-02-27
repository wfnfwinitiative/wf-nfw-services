from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.hunger_spot_schemas import (
    HungerSpotCreate,
    HungerSpotRead,
    HungerSpotUpdate,
)
from app.services.hunger_spot_service import HungerSpotService
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/hunger-spots", tags=["Hunger Spots"])


@router.post("/", response_model=HungerSpotRead)
async def create_spot(
    payload: HungerSpotCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return await HungerSpotService(db).create_hunger_spot(
        creator_id=current_user.user_id,
        **payload.dict(),
    )


@router.get("/", response_model=list[HungerSpotRead])
async def get_spots(db: AsyncSession = Depends(get_db)):
    return await HungerSpotService(db).get_all_hunger_spots()


@router.get("/{hunger_spot_id}", response_model=HungerSpotRead)
async def get_spot(hunger_spot_id: int, db: AsyncSession = Depends(get_db)):
    return await HungerSpotService(db).get_hunger_spot(hunger_spot_id)


@router.patch("/{hunger_spot_id}", response_model=HungerSpotRead)
async def update_spot(hunger_spot_id: int, payload: HungerSpotUpdate, db: AsyncSession = Depends(get_db)):
    return await HungerSpotService(db).update_hunger_spot(
        hunger_spot_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{hunger_spot_id}")
async def delete_spot(hunger_spot_id: int, db: AsyncSession = Depends(get_db)):
    return await HungerSpotService(db).delete_hunger_spot(hunger_spot_id)