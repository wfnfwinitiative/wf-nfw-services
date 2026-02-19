from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.user import User
from typing import List, Optional
from uuid import UUID


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> List[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get(self, user_id: UUID) -> Optional[User]:
        result = await self.session.get(User, user_id)
        return result

    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, **kwargs) -> User:
        for k, v in kwargs.items():
            setattr(user, k, v)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
