from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.role_schemas import RoleRead
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RoleRead])
async def get_roles(db: AsyncSession = Depends(get_db)):
    return await RoleService(db).get_all_roles()


@router.get("/{role_id}", response_model=RoleRead)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    roles = await RoleService(db).get_all_roles()
    return next((r for r in roles if r.role_id == role_id), None)