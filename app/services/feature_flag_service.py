from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.feature_flag_repository import FeatureFlagRepository
from app.entities.feature_flag_entities import FeatureFlag


class FeatureFlagService:
    def __init__(self, db: AsyncSession):
        self.repository = FeatureFlagRepository(db)
        self.db = db

    async def create_feature_flag(self, feature_flag_name: str, enabled: bool = False) -> FeatureFlag:
        """Create a new feature flag"""
        # Check if flag already exists
        existing_flag = await self.repository.get_by_name(feature_flag_name)
        if existing_flag:
            raise HTTPException(status_code=400, detail="Feature flag already exists")

        flag = await self.repository.create(feature_flag_name, enabled)
        await self.db.commit()
        return flag

    async def get_feature_flag(self, flag_id: int) -> FeatureFlag:
        """Get a feature flag by ID"""
        flag = await self.repository.get_by_id(flag_id)
        if not flag:
            raise HTTPException(status_code=404, detail="Feature flag not found")
        return flag

    async def get_feature_flag_by_name(self, feature_flag_name: str) -> FeatureFlag:
        """Get a feature flag by name"""
        flag = await self.repository.get_by_name(feature_flag_name)
        if not flag:
            raise HTTPException(status_code=404, detail="Feature flag not found")
        return flag

    async def get_all_feature_flags(self) -> list[FeatureFlag]:
        """Get all feature flags"""
        return await self.repository.get_all()

    async def update_feature_flag(self, flag_id: int, enabled: bool) -> FeatureFlag:
        """Update feature flag enabled status"""
        flag = await self.repository.get_by_id(flag_id)
        if not flag:
            raise HTTPException(status_code=404, detail="Feature flag not found")

        updated_flag = await self.repository.update(flag_id, enabled)
        await self.db.commit()
        return updated_flag

    async def delete_feature_flag(self, flag_id: int) -> dict:
        """Delete a feature flag"""
        flag = await self.repository.get_by_id(flag_id)
        if not flag:
            raise HTTPException(status_code=404, detail="Feature flag not found")

        await self.repository.delete(flag_id)
        await self.db.commit()
        return {"message": "Feature flag deleted successfully"}
