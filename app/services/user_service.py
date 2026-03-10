from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.core.security import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.user_role_repo = UserRoleRepository(db)
        self.db = db

    async def create_user_with_role(self, name: str, mobile_number: str, password: str, role_name: str):
        existing = await self.repo.get_by_mobile(mobile_number)
        if existing:
            raise HTTPException(status_code=400, detail="Mobile number already registered")

        role = await self.role_repo.get_by_name(role_name)
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role name")

        password_hash = hash_password(password)

        user = await self.repo.create(name, mobile_number, password_hash)
        await self.db.commit()

        # Ensure the role assignment is persisted and the response can access it without
        # triggering lazy-load after the session is closed.
        await self.user_role_repo.assign_role(user.user_id, role.role_id)
        await self.db.commit()

        return {
            "user_id": user.user_id,
            "name": user.name,
            "mobile_number": user.mobile_number,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": [role.role_name],
        }

    async def get_user(self, user_id: int):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Return a plain dict so FastAPI/Pydantic doesn't try to lazy-load relationships
        # after the DB session has been closed.
        return {
            "user_id": user.user_id,
            "name": user.name,
            "mobile_number": user.mobile_number,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": [role.role_name for role in user.roles],
        }

    async def get_user_by_mobile(self, phone_number: str):
        user = await self.repo.get_by_mobile(phone_number)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": user.user_id,
            "name": user.name,
            "mobile_number": user.mobile_number,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": [role.role_name for role in user.roles],
        }

    async def get_all_users(self):
        users = await self.repo.get_all()
        return [
            {
                "user_id": user.user_id,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "roles": [role.role_name for role in user.roles]
            }
            for user in users
        ]
    async def get_users_by_role(self, role_name: str):
        users = await self.repo.get_by_role_name(role_name)
        return [
            {
                "user_id": user.user_id,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "roles": [role.role_name for role in user.roles]
            }
            for user in users
        ]
    async def get_users_by_role(self, role_name: str):
        users = await self.repo.get_by_role_name(role_name)
        return [
            {
                "user_id": user.user_id,
                "name": user.name,
                "mobile_number": user.mobile_number,
                "is_active": user.is_active,
                "created_at": user.created_at,
                "roles": [role.role_name for role in user.roles]
            }
            for user in users
        ]

    async def deactivate_user(self, user_id: int):
        user = await self.repo.deactivate(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.db.commit()
        return {"message": "User deactivated"}
