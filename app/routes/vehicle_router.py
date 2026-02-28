from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.vehicle_schemas import (
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)
from app.services.vehicle_service import VehicleService
# from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleRead)
async def create_vehicle(
    payload: VehicleCreate,
    db: AsyncSession = Depends(get_db),
    # current_user=Depends(get_current_user),
):
    return await VehicleService(db).create_vehicle(
        creator_id=4,
        vehicle_no=payload.vehicle_no,
        notes=payload.notes,
    )


@router.get("/", response_model=list[VehicleRead])
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    return await VehicleService(db).get_all_vehicles()


@router.get("/{vehicle_id}", response_model=VehicleRead)
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    return await VehicleService(db).get_vehicle(vehicle_id)


@router.patch("/{vehicle_id}", response_model=VehicleRead)
async def update_vehicle(vehicle_id: int, payload: VehicleUpdate, db: AsyncSession = Depends(get_db)):
    return await VehicleService(db).update_vehicle(
        vehicle_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    return await VehicleService(db).delete_vehicle(vehicle_id)