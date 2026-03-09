from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.status_schemas import StatusCreate, StatusRead, StatusUpdate
from app.services.status_service import StatusService

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.post("/", response_model=StatusRead)
async def create_status(
    payload: StatusCreate,
    db: AsyncSession = Depends(get_db),
):
    return await StatusService(db).create_status(payload.status_name)


@router.get("/", response_model=list[StatusRead])
async def get_statuses(db: AsyncSession = Depends(get_db)):
    return await StatusService(db).get_all_statuses()


@router.get("/{status_id}", response_model=StatusRead)
async def get_status(status_id: int, db: AsyncSession = Depends(get_db)):
    return await StatusService(db).get_status(status_id)


@router.patch("/{status_id}", response_model=StatusRead)
async def update_status(status_id: int, payload: StatusUpdate, db: AsyncSession = Depends(get_db)):
    return await StatusService(db).update_status(status_id, payload.status_name)


@router.delete("/{status_id}")
async def delete_status(status_id: int, db: AsyncSession = Depends(get_db)):
    return await StatusService(db).delete_status(status_id)
