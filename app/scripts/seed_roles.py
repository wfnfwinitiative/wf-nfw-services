import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import engine

# make sure related tables and classes are registered in metadata before Role's relationships
from app.models import user_role_models  # noqa: F401
from app.models import user_models       # noqa: F401
from app.models.role_models import Role

ROLES = ["ADMIN", "COORDINATOR", "DRIVER"]


async def seed_roles():
    async with AsyncSession(engine) as db:
        for role_name in ROLES:
            result = await db.execute(text(f"SELECT role_id, role_name FROM {Role.__table_args__['schema']}.roles WHERE role_name = :name"), {"name": role_name})
            existing = result.scalar_one_or_none()

            if not existing:
                db.add(Role(role_name=role_name))
                print(f"Inserted role: {role_name}")
            else:
                print(f"Role already exists: {role_name}")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_roles())
