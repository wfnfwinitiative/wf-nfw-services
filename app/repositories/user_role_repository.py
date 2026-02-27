from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_role_models import UserRole
from app.models.role_models import Role


class UserRoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def assign_role(self, user_id: int, role_id: int):
        obj = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_roles_for_user(self, user_id: int):
        result = await self.db.execute(
            select(Role.role_name)
            .join(UserRole, Role.role_id == UserRole.role_id)
            .where(UserRole.user_id == user_id)
        )
        return result.scalars().all()

    async def remove_role(self, user_id: int, role_id: int):
        result = await self.db.execute(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            )
        )
        obj = result.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
            await self.db.flush()
            return True
        return False