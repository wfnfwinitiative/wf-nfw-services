import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# ==============================
# CONFIG (UPDATE THESE)
# ==============================

from app.db.session import engine
from app.core.config import settings

# ==========================
# DATABASE CONFIG
# ==========================
SCHEMA = settings.DB_SCHEMA

# ==============================
# MIGRATION SCRIPT
# ==============================


async def apply_changes():
    async with AsyncSession(engine) as conn:

        # ==========================
        # CHECK CONSTRAINTS (Safe)
        # ==========================

        await conn.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'check_mobile_format'
            ) THEN
                ALTER TABLE {SCHEMA}.users
                ADD CONSTRAINT check_mobile_format
                CHECK (mobile_number ~ '^[6-9][0-9]{{9}}$');
            END IF;
        END$$;
        """))

        await conn.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'check_vehicle_not_empty'
            ) THEN
                ALTER TABLE {SCHEMA}.vehicles
                ADD CONSTRAINT check_vehicle_not_empty
                CHECK (length(trim(vehicle_no)) > 0);
            END IF;
        END$$;
        """))

        await conn.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'check_feeding_positive'
            ) THEN
                ALTER TABLE {SCHEMA}.opportunities
                ADD CONSTRAINT check_feeding_positive
                CHECK (feeding_count >= 0);
            END IF;
        END$$;
        """))

        await conn.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'check_quantity_positive'
            ) THEN
                ALTER TABLE {SCHEMA}.opportunity_items
                ADD CONSTRAINT check_quantity_positive
                CHECK (quantity_value >= 0);
            END IF;
        END$$;
        """))

        # ==========================
        # INDEXES (Safe)
        # ==========================

        await conn.execute(text(f"""
        CREATE INDEX IF NOT EXISTS idx_user_mobile
        ON {SCHEMA}.users(mobile_number);
        """))

        await conn.execute(text(f"""
        CREATE INDEX IF NOT EXISTS idx_opportunity_status
        ON {SCHEMA}.opportunities(status_id);
        """))

        await conn.execute(text(f"""
        CREATE INDEX IF NOT EXISTS idx_opportunity_donor
        ON {SCHEMA}.opportunities(donor_id);
        """))

        # ==========================
        # UNIQUE USER ROLE MAPPING
        # ==========================

        await conn.execute(text(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'unique_user_role'
            ) THEN
                ALTER TABLE {SCHEMA}.user_roles
                ADD CONSTRAINT unique_user_role
                UNIQUE (user_id, role_id);
            END IF;
        END$$;
        """))

        # ==========================
        # UPDATED_AT TRIGGER FUNCTION
        # ==========================

        await conn.execute(text(f"""
        CREATE OR REPLACE FUNCTION {SCHEMA}.update_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """))

        tables_with_updated = ["users", "vehicles", "donors", "opportunities"]

        for table in tables_with_updated:
            await conn.execute(text(f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_trigger
                    WHERE tgname = 'trg_{table}_updated'
                ) THEN
                    CREATE TRIGGER trg_{table}_updated
                    BEFORE UPDATE ON {SCHEMA}.{table}
                    FOR EACH ROW
                    EXECUTE FUNCTION {SCHEMA}.update_timestamp();
                END IF;
            END$$;
            """))

        print("Database hardening applied successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(apply_changes())
