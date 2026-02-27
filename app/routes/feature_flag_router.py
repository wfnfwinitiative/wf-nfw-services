from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import require_role
from app.schemas.feature_flag_schemas import FeatureFlagCreate, FeatureFlagUpdate, FeatureFlagRead
from app.services.feature_flag_service import FeatureFlagService

router = APIRouter(
    prefix="/api/feature-flags", tags=["Feature Flags"]
)


# ============================================
# CREATE FEATURE FLAG (ADMIN ONLY)
# ============================================
@router.post("", response_model=FeatureFlagRead, dependencies=[Depends(require_role(["ADMIN"]))])
async def create_feature_flag(
    data: FeatureFlagCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new feature flag (Admin only)"""
    service = FeatureFlagService(db)
    flag = await service.create_feature_flag(data.feature_flag_name, data.enabled)
    return flag


# ============================================
# GET ALL FEATURE FLAGS
# ============================================
@router.get("", response_model=list[FeatureFlagRead])
async def get_all_feature_flags(db: AsyncSession = Depends(get_db)):
    """Get all feature flags"""
    service = FeatureFlagService(db)
    flags = await service.get_all_feature_flags()
    return flags


# ============================================
# GET FEATURE FLAG BY NAME
# ============================================
@router.get("/{feature_flag_name}", response_model=FeatureFlagRead)
async def get_feature_flag_by_name(
    feature_flag_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a feature flag by name"""
    service = FeatureFlagService(db)
    flag = await service.get_feature_flag_by_name(feature_flag_name)
    return flag


# ============================================
# GET FEATURE FLAG BY ID
# ============================================
@router.get("/{flag_id}", response_model=FeatureFlagRead)
async def get_feature_flag(flag_id: int, db: AsyncSession = Depends(get_db)):
    """Get a feature flag by ID"""
    service = FeatureFlagService(db)
    flag = await service.get_feature_flag(flag_id)
    return flag


# ============================================
# UPDATE FEATURE FLAG (ADMIN ONLY)
# ============================================
@router.put("/{flag_id}", response_model=FeatureFlagRead, dependencies=[Depends(require_role(["ADMIN"]))])
async def update_feature_flag(
    flag_id: int,
    data: FeatureFlagUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update feature flag enabled status (Admin only)"""
    service = FeatureFlagService(db)
    flag = await service.update_feature_flag(flag_id, data.enabled)
    return flag


# ============================================
# DELETE FEATURE FLAG (ADMIN ONLY)
# ============================================
@router.delete("/{flag_id}", dependencies=[Depends(require_role(["ADMIN"]))])
async def delete_feature_flag(flag_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a feature flag (Admin only)"""
    service = FeatureFlagService(db)
    result = await service.delete_feature_flag(flag_id)
    return result
