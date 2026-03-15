from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import UserRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.user_role_repository import UserRoleRepository
from app.core.security import hash_password, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.role_repo = RoleRepository(db)
        self.user_role_repo = UserRoleRepository(db)
        self.db = db

    async def create_user_with_role(
        self,
        name: str,
        mobile_number: str,
        password: str,
        role_name: str,
        email: str = None,
        caller: dict = None,
    ):
        """Create a user with a role.

        Access rules:
        - If no users exist: caller must be SUPPORTADMIN (breakglass login).
        - If users exist: caller must be authenticated ADMIN.
        """

        if not caller:
            raise HTTPException(status_code=401, detail="Authentication required")

        all_users = await self.repo.get_all()
        has_users = len(all_users) > 0

        user_roles = caller.get("role") or []
        user_roles = user_roles if isinstance(user_roles, list) else [user_roles]

        if not has_users:
            # Fresh DB — only SUPPORTADMIN (breakglass) can create first ADMIN
            if not any(r in ["SUPPORTADMIN"] for r in user_roles):
                raise HTTPException(status_code=403, detail="Only SUPPORTADMIN can create the first user")
            if role_name != "ADMIN":
                raise HTTPException(status_code=403, detail="First user must be an ADMIN")
        else:
            # Users exist — require authenticated ADMIN caller
            if not any(r in ["ADMIN", "SUPPORTADMIN"] for r in user_roles):
                raise HTTPException(status_code=403, detail="Only ADMIN can create users")

        existing = await self.repo.get_by_mobile(mobile_number)
        if existing:
            raise HTTPException(status_code=400, detail="Mobile number already registered")

        role = await self.role_repo.get_by_name(role_name)
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role name")

        password_hash = hash_password(password)

        user = await self.repo.create(name, mobile_number, password_hash, email=email)
        await self.db.commit()

        await self.user_role_repo.assign_role(user.user_id, role.role_id)
        await self.db.commit()

        return {
            "user_id": user.user_id,
            "name": user.name,
            "mobile_number": user.mobile_number,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": [role.role_name],
        }

    async def reset_admin_password(
        self,
        mobile_number: str,
        new_password: str,
        caller: dict = None,
    ):
        """Reset an ADMIN user's password. Only SUPPORTADMIN can do this."""
        if not caller:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        user_roles = caller.get("role") or []
        user_roles = user_roles if isinstance(user_roles, list) else [user_roles]

        if "SUPPORTADMIN" not in user_roles:
            raise HTTPException(status_code=403, detail="Only SUPPORTADMIN can reset admin password")

        user = await self.repo.get_by_mobile(mobile_number)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify user is an ADMIN
        role_names = [r.role_name for r in user.roles]
        if "ADMIN" not in role_names:
            raise HTTPException(status_code=403, detail="Password reset is only for ADMIN accounts")

        user.password_hash = hash_password(new_password)
        await self.db.commit()

        return {"message": f"Password reset successfully for {mobile_number}"}

    async def change_password(
        self,
        current_password: str,
        new_password: str,
        caller: dict = None,
    ):
        """User changes their own password. Must provide current password."""
        if not caller:
            raise HTTPException(status_code=401, detail="Authentication required")

        user = await self.repo.get_by_id(caller.get("user_id"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        user.password_hash = hash_password(new_password)
        await self.db.commit()

        return {"message": "Password changed successfully"}

    async def unlock_user(
        self,
        user_id: int,
        caller: dict = None,
    ):
        """ADMIN unlocks a user: resets password to a default and reactivates."""
        if not caller:
            raise HTTPException(status_code=401, detail="Authentication required")

        user_roles = caller.get("role") or []
        user_roles = user_roles if isinstance(user_roles, list) else [user_roles]


        if "ADMIN" not in user_roles and "SUPPORTADMIN" not in user_roles:
            raise HTTPException(status_code=403, detail="Only ADMIN or SUPPORTADMIN can unlock users")

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        default_password = "Welcome@123"
        user.password_hash = hash_password(default_password)
        user.is_active = True
        await self.db.commit()

        return {
            "message": f"User {user.name} unlocked with default password",
            "default_password": default_password,
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
            "email": user.email,
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
            "email": user.email,
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
                "email": user.email,
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
                "email": user.email,
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
                "email": user.email,
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

    async def activate_user(self, user_id: int):
        user = await self.repo.activate(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.db.commit()
        return {"message": "User activated"}


    async def update_user(self, user_id: int, **data):
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        password = data.pop("password", None)
        if password:
            data["password_hash"] = hash_password(password)

        print(password)
        print(data)

        user = await self.repo.update(user_id, **data)
        await self.db.commit()
        return {
            "user_id": user.user_id,
            "name": user.name,
            "mobile_number": user.mobile_number,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "roles": [role.role_name for role in user.roles],
        }
