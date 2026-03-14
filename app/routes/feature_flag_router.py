from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.dependencies.auth import require_roles
from app.schemas.feature_flag_schemas import (
    FeatureFlagCreate,
    FeatureFlagUpdate,
    FeatureFlagRead,
)
from app.services.feature_flag_service import FeatureFlagService

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])


# ============================================
# CREATE FEATURE FLAG
# ============================================
@router.post(
    "", response_model=FeatureFlagRead, dependencies=[Depends(require_roles(["ADMIN"]))]
)
async def create_feature_flag(
    data: FeatureFlagCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new feature flag"""
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
    db: AsyncSession = Depends(get_db),
):
    """Get a feature flag by name"""
    service = FeatureFlagService(db)
    flag = await service.get_feature_flag_by_name(feature_flag_name)
    return flag


# Note: retrieval by ID is no longer supported via the router; the name
# is treated as the unique identifier for flags.


# ============================================
# UPDATE FEATURE FLAG
# ============================================
@router.patch(
    "/{feature_flag_name}",
    response_model=FeatureFlagRead,
    dependencies=[Depends(require_roles(["ADMIN"]))],
)
async def update_feature_flag(
    feature_flag_name: str,
    data: FeatureFlagUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update feature flag enabled status by name"""
    service = FeatureFlagService(db)
    flag = await service.update_feature_flag(feature_flag_name, data.enabled)
    return flag


# ============================================
# DELETE FEATURE FLAG
# ============================================
@router.delete(
    "/{feature_flag_name}",
    dependencies=[Depends(require_roles(["ADMIN"]))],
)
async def delete_feature_flag(
    feature_flag_name: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a feature flag by name"""
    service = FeatureFlagService(db)
    result = await service.delete_feature_flag(feature_flag_name)
    return result
