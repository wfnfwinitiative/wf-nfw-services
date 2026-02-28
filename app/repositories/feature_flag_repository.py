from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.feature_flag_models import FeatureFlag


class FeatureFlagRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, feature_flag_name: str, enabled: bool = False) -> FeatureFlag:
        """Create a new feature flag"""
        flag = FeatureFlag(feature_flag_name=feature_flag_name, enabled=enabled)
        self.db.add(flag)
        await self.db.flush()
        return flag

    async def get_by_id(self, flag_id: int) -> FeatureFlag:
        """Get feature flag by ID"""
        result = await self.db.execute(
            select(FeatureFlag).where(FeatureFlag.id == flag_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, feature_flag_name: str) -> FeatureFlag:
        """Get feature flag by name"""
        result = await self.db.execute(
            select(FeatureFlag).where(FeatureFlag.feature_flag_name == feature_flag_name)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[FeatureFlag]:
        """Get all feature flags"""
        result = await self.db.execute(select(FeatureFlag))
        return result.scalars().all()

    async def update(self, flag_id: int, enabled: bool) -> FeatureFlag:
        """Update feature flag enabled status"""
        flag = await self.get_by_id(flag_id)
        if flag:
            flag.enabled = enabled
            await self.db.flush()
        return flag

    async def update_by_name(self, feature_flag_name: str, enabled: bool) -> FeatureFlag:
        """Update feature flag enabled status using name"""
        flag = await self.get_by_name(feature_flag_name)
        if flag:
            flag.enabled = enabled
            await self.db.flush()
        return flag

    async def delete(self, flag_id: int) -> bool:
        """Delete a feature flag"""
        flag = await self.get_by_id(flag_id)
        if flag:
            await self.db.delete(flag)
            await self.db.flush()
            return True
        return False

    async def delete_by_name(self, feature_flag_name: str) -> bool:
        """Delete a feature flag using name"""
        flag = await self.get_by_name(feature_flag_name)
        if flag:
            await self.db.delete(flag)
            await self.db.flush()
            return True
        return False
