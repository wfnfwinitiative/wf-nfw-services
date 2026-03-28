from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.report_schemas import ReportFilterRequest
from app.services.report_service import ReportService
from app.db.session import get_db

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.post("/opportunities")
async def get_opportunity_report(
    filters: ReportFilterRequest,
    db: AsyncSession = Depends(get_db)
):
    service = ReportService(db)
    return await service.get_report(filters)