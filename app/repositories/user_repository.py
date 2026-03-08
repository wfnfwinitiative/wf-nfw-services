from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_models import User
from sqlalchemy.orm import selectinload


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, mobile_number: str, password_hash: str):
        user = User(
            name=name,
            mobile_number=mobile_number,
            password_hash=password_hash
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_mobile(self, mobile_number: str):
        result = await self.db.execute(
            select(User).where(User.mobile_number == mobile_number)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(User).options(selectinload(User.roles))
        )
        return result.scalars().all()

    async def deactivate(self, user_id: int):
        user = await self.get_by_id(user_id)
        if user:
            user.is_active = False
            await self.db.flush()
        return user