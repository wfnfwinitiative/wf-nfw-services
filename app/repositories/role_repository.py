from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.role_models import Role


class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Role))
        return result.scalars().all()


    async def get_by_name(self, role_name: str):
        result = await self.db.execute(
            select(Role).where(Role.role_name == role_name)
        )
        return result.scalar_one_or_none()