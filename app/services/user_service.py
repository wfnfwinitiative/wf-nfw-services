from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from app.repositories.user_repository import UserRepository
from app.models.user_models import User
from app.models.user_role_models import UserRole
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

    async def get_drivers(self):
        """Get all users with driver role (role_id=3)"""
        try:
            print('hi')
            result = await self.db.execute(
                select(User).join(
                    UserRole, User.user_id == UserRole.user_id
                ).where(UserRole.role_id == 3)
            )
            print(result)
            return result.scalars().all()
        except Exception as err:
            print(err)
            raise HTTPException(status_code=500, detail=err)

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