from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.user_role_service import UserRoleService
from app.dependencies.auth import require_roles

router = APIRouter(prefix="/user-roles", tags=["User Roles"])


@router.post("/")
async def assign_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    return await UserRoleService(db).assign_role(user_id, role_id)


@router.delete("/")
async def remove_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db)):
    return await UserRoleService(db).remove_role(user_id, role_id)