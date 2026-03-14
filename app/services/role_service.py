from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.role_repository import RoleRepository


class RoleService:
    def __init__(self, db: AsyncSession):
        self.repo = RoleRepository(db)

    async def get_all_roles(self):
        return await self.repo.get_all()
