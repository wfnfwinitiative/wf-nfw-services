from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.status_schemas import StatusRead
from app.services.status_service import StatusService

router = APIRouter(prefix="/statuses", tags=["Statuses"])


@router.get("/", response_model=list[StatusRead])
async def get_statuses(db: AsyncSession = Depends(get_db)):
    return await StatusService(db).get_all_statuses()