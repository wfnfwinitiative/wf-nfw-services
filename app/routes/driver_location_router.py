from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.driver_location_schemas import DriverLocationUpsert, DriverLocationRead
from app.services.driver_location_service import DriverLocationService
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/driver-locations", tags=["Driver Locations"])


@router.put("/{opportunity_id}", response_model=DriverLocationRead)
async def update_driver_location(
    opportunity_id: int,
    payload: DriverLocationUpsert,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["DRIVER"])),
):
    """Driver sends their current GPS position for an active opportunity."""
    return await DriverLocationService(db).update_location(
        opportunity_id=opportunity_id,
        driver_id=caller["user_id"],
        latitude=payload.latitude,
        longitude=payload.longitude,
        accuracy=payload.accuracy,
    )


@router.get("/{opportunity_id}", response_model=DriverLocationRead)
async def get_driver_location(
    opportunity_id: int,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR"])),
):
    """Coordinator polls for the driver's latest GPS position."""
    return await DriverLocationService(db).get_location(opportunity_id)
