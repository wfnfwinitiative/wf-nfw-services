import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import engine
from app.models.status_models import Status

# list of (name, info) pairs based on workflow descriptions
STATUSES = [
    ("Created", "When an Admin creates a new opportunity."),
    ("Assigned", "When an Admin assigns the opportunity to a driver."),
    ("InPickup", "When the driver picks up the assigned opportunity."),
    ("Rejected", "When the driver rejects the opportunity."),
    ("Delivered", "When the driver marks the opportunity as delivered."),
    ("Verified", "When the coordinator verifies a submitted opportunity."),
    ("Completed", "When the coordinator updates the status to completed."),
]


async def seed_statuses():
    async with AsyncSession(engine) as db:
        for name, info in STATUSES:
            result = await db.execute(select(Status).where(Status.status_name == name))
            existing = result.scalar_one_or_none()

            if not existing:
                db.add(Status(status_name=name, status_info=info))
                print(f"Inserted status: {name}")
            else:
                print(f"Status already exists: {name}")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed_statuses())
