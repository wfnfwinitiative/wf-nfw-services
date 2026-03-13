import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import engine, Base
from app.core.config import settings

# import all model modules to register tables with Base.metadata
from app.models import (
    donor_models,
    feature_flag_models,
    hunger_spot_models,
    opportunity_allocation_models,
    opportunity_event_models,
    opportunity_item_models,
    opportunity_models,
    role_models,
    status_models,
    user_models,
    user_role_models,
    vehicle_models,
)

# bring in existing helpers (keeping single-seed logic centralized)
from app.scripts.seed_roles import seed_roles
from app.scripts.seed_statuses import seed_statuses
from app.scripts.db_constraints import apply_changes

SCHEMA = settings.DB_SCHEMA


async def full_reset():
    print("Starting full database reset...")

    async with engine.begin() as conn:
        print(f"Dropping schema '{SCHEMA}' with CASCADE...")
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {SCHEMA} CASCADE"))

        print(f"Creating schema '{SCHEMA}'...")
        await conn.execute(text(f"CREATE SCHEMA {SCHEMA}"))

        print("Creating tables one by one...")
        for table in Base.metadata.sorted_tables:
            print(f"   → Creating table: {table.schema}.{table.name}")
            await conn.run_sync(lambda sync_session: table.create(bind=sync_session))

    print("Disposing engine to clear caches...")
    await engine.dispose()

    print("Applying constraints and indexes...")
    await apply_changes()

    print("Disposing engine again before seeding...")
    await engine.dispose()

    print("Seeding lookup tables...")
    await seed_roles()
    await seed_statuses()

    print("Database dropped, recreated, hardened, and seeded successfully!")


if __name__ == "__main__":
    asyncio.run(full_reset())
