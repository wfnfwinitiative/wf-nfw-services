from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_role_repository import UserRoleRepository


class UserRoleService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRoleRepository(db)
        self.db = db

    async def assign_role(self, user_id: int, role_id: int):
        await self.repo.assign_role(user_id, role_id)
        await self.db.commit()
        return {"message": "Role assigned"}

    async def remove_role(self, user_id: int, role_id: int):
        if not await self.repo.remove_role(user_id, role_id):
            raise HTTPException(status_code=404, detail="Role mapping not found")
        await self.db.commit()
        return {"message": "Role removed"}
