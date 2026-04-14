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
from app.scripts.seed_feature_flags import seed_feature_flags
from app.scripts.db_constraints import apply_changes
from app.scripts.seed_test_data import seed_test_data, seed_inital_admin_coord_driver


SCHEMA = settings.DB_SCHEMA
import sys


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
    await seed_feature_flags()

    print("Database dropped, recreated, hardened, and seeded successfully!")


async def full_reset_with_test_data():
    """Full reset + seed test data (users, donors, hunger spots, vehicles)"""
    await full_reset()
    
    print("\n" + "="*60)
    print("Seeding test data...")
    print("="*60 + "\n")
    
    await seed_test_data()


async def main():
    include_test_data = "--with-test-data" in sys.argv or "-t" in sys.argv
    include_initial_accounts = "--with-initial-accounts" in sys.argv or "-a" in sys.argv

    print("\n" + "="*60)
    print("Resetting the database and seeding lookup tables (roles, statuses, feature flags)...")
    await full_reset()

    if include_initial_accounts:
        print("\n" + "="*60)
        print("Seeding initial accounts (admin, coordinator, driver)...")
        print("="*60 + "\n")
        await seed_inital_admin_coord_driver()

    if include_test_data:
        print("\n" + "="*60)
        print("Seeding full test data (users, donors, hunger spots, vehicles)...")
        print("="*60 + "\n")
        await seed_test_data()


if __name__ == "__main__":
    asyncio.run(main())
    
    