import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import engine
from app.models.feature_flag_models import FeatureFlag

FEATURE_FLAGS = [
    "voice_llm_service",
    "voice_support",
    "google_image_upload",
]


async def seed_feature_flags():
    async with AsyncSession(engine) as db:
        schema = FeatureFlag.__table_args__["schema"]
        for flag_name in FEATURE_FLAGS:
            result = await db.execute(
                text(f"SELECT id FROM {schema}.feature_flags WHERE feature_flag_name = :name"),
                {"name": flag_name},
            )
            existing = result.scalar_one_or_none()

            if not existing:
                db.add(FeatureFlag(feature_flag_name=flag_name, enabled=True))
                print(f"Inserted feature flag: {flag_name}")
            else:
                print(f"Feature flag already exists: {flag_name}")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_feature_flags())
