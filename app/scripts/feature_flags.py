import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import engine
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA

# Change this to your admin/system user id
DEFAULT_CREATOR_ID = 1


TABLES_TO_UPDATE = [
    "vehicles",
    "donors",
    "hunger_spots",
    "opportunities",
]


async def apply_changes():
    async with AsyncSession(engine) as conn:

        # -------------------------------------------------
        # 1️⃣ Create feature_flags table
        # -------------------------------------------------
        await conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {SCHEMA}.feature_flags (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                feature_flag_name VARCHAR(100) UNIQUE NOT NULL,
                enabled BOOLEAN NOT NULL DEFAULT FALSE,

                creator_id BIGINT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

                CONSTRAINT fk_feature_flags_creator
                    FOREIGN KEY (creator_id)
                    REFERENCES {SCHEMA}.users(user_id)
            );
        """))

        # -------------------------------------------------
        # 2️⃣ Add creator_id to existing tables
        # -------------------------------------------------
        for table in TABLES_TO_UPDATE:

            print(f"Updating table: {table}")

            # Add column if not exists
            await conn.execute(text(f"""
                ALTER TABLE {SCHEMA}.{table}
                ADD COLUMN IF NOT EXISTS creator_id BIGINT;
            """))

            # Backfill existing rows
            await conn.execute(text(f"""
                UPDATE {SCHEMA}.{table}
                SET creator_id = :default_id
                WHERE creator_id IS NULL;
            """), {"default_id": DEFAULT_CREATOR_ID})

            # Add FK constraint (safe — will fail silently if exists)
            await conn.execute(text(f"""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conname = 'fk_{table}_creator'
                    ) THEN
                        ALTER TABLE {SCHEMA}.{table}
                        ADD CONSTRAINT fk_{table}_creator
                        FOREIGN KEY (creator_id)
                        REFERENCES {SCHEMA}.users(user_id);
                    END IF;
                END
                $$;
            """))

            # Make column NOT NULL
            await conn.execute(text(f"""
                ALTER TABLE {SCHEMA}.{table}
                ALTER COLUMN creator_id SET NOT NULL;
            """))

            # Add index
            await conn.execute(text(f"""
                CREATE INDEX IF NOT EXISTS idx_{table}_creator_id
                ON {SCHEMA}.{table}(creator_id);
            """))

        await conn.commit()

    print("✅ Feature flag table created and creator_id added to all tables!")


if __name__ == "__main__":
    asyncio.run(apply_changes())