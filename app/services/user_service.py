from app.repositories.user_repository import UserRepository
from app.entities.user import User
from app.models import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID


class UserService:
    def __init__(self, session: AsyncSession):
        self.repo = UserRepository(session)

    async def list_users(self) -> List[User]:
        return await self.repo.list()

    async def get_user(self, user_id: UUID) -> Optional[User]:
        return await self.repo.get(user_id)

    async def create_user(self, payload: UserCreate) -> User:
        user = User(email=payload.email, phone=payload.phone, name=payload.name)
        return await self.repo.create(user)

    async def update_user(self, user_id: UUID, payload: UserUpdate) -> Optional[User]:
        user = await self.repo.get(user_id)
        if not user:
            return None
        data = payload.dict(exclude_unset=True)
        return await self.repo.update(user, **data)

    async def delete_user(self, user_id: UUID) -> bool:
        user = await self.repo.get(user_id)
        if not user:
            return False
        await self.repo.delete(user)
        return True
