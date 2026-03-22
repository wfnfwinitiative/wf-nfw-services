from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.user_role_repository import UserRoleRepository


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db=db)
        self.user_role_repository = UserRoleRepository(db=db)

    async def authenticate_user(self, mobile: str, password: str):

        # Check if this is a breakglass login
        if mobile == settings.BREAKGLASS_MOBILE:
            return self._authenticate_breakglass(password)

        # 1️⃣ Fetch user
        user = await self.user_repository.get_by_mobile(mobile)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # 2️⃣ Verify password
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # 3️⃣ Fetch role
        user_roles = await self.user_role_repository.get_roles_for_user(user.user_id)
        if not user_roles:
            raise HTTPException(status_code=403, detail="User has no assigned role")

        # 4️⃣ Create token with role
        token = create_access_token(user_id=user.user_id, name=user.name, role=sorted(user_roles))

        return token

    @staticmethod
    def _authenticate_breakglass(password: str) -> str:
        """Authenticate the breakglass admin using env-stored password hash."""
        if not settings.BREAKGLASS_PASSWORD_HASH:
            raise HTTPException(status_code=500, detail="Breakglass not configured on server")

        if not verify_password(password, settings.BREAKGLASS_PASSWORD_HASH):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return token with special SUPPORTADMIN role and user_id=0
        token = create_access_token(user_id=0, name="SUPPORTADMIN", role=["SUPPORTADMIN"])
        return token
