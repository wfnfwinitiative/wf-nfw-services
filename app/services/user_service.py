from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.db = db

    async def create_user(self, name: str, mobile_number: str, password: str):
        existing = await self.repo.get_by_mobile(mobile_number)
        if existing:
            raise HTTPException(status_code=400, detail="Mobile number already registered")

        password_hash = hash_password(password)

        user = await self.repo.create(name, mobile_number, password_hash)
        await self.db.commit()
        return user

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_user_by_mobile(self, phone_number: str):
        user = await self.repo.get_by_mobile(phone_number)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            return user

    async def get_all_users(self):
        return await self.repo.get_all()

    async def deactivate_user(self, user_id: int):
        user = await self.repo.deactivate(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.db.commit()
        return {"message": "User deactivated"}