from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_models import User
from sqlalchemy.orm import selectinload
from app.models.user_role_models import UserRole


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, mobile_number: str, password_hash: str, email: str = None):
        user = User(
            name=name,
            mobile_number=mobile_number,
            password_hash=password_hash,
            email=email,
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_mobile(self, mobile_number: str):
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.roles))
            .where(User.mobile_number == mobile_number)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(User).options(selectinload(User.roles))
        )
        return result.scalars().all()

    async def get_by_role_name(self, role_name: str):
        from app.models.role_models import Role
        result = await self.db.execute(
            select(User).join(UserRole).join(Role).where(Role.role_name == role_name).options(selectinload(User.roles))
        )
        return result.scalars().all()

    async def deactivate(self, user_id: int):
        user = await self.get_by_id(user_id)
        if user:
            user.is_active = False
            await self.db.flush()
        return user

    async def activate(self, user_id: int):
        user = await self.get_by_id(user_id)
        if user:
            user.is_active = True
            await self.db.flush()
        return user

    async def update(self, user_id: int, **kwargs):
        user = await self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.db.flush()
        return user