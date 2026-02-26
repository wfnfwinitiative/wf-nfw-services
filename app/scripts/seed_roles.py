import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import engine
from app.entities.entities import Role

ROLES = ["ADMIN", "COORDINATOR", "DRIVER"]


async def seed_roles():
    async with AsyncSession(engine) as db:
        for role_name in ROLES:

            result = await db.execute(select(Role).where(Role.role_name == role_name))
            existing = result.scalar_one_or_none()

            if not existing:
                db.add(Role(role_name=role_name))
                print(f"Inserted role: {role_name}")
            else:
                print(f"Role already exists: {role_name}")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_roles())
