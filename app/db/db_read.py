from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.entities.entities import Role, User, UserRole


async def get_role_by_name(db: AsyncSession, role_name: str):
    result = await db.execute(select(Role).where(Role.role_name == role_name.upper()))
    return result.scalar_one_or_none()


async def get_user_by_mobile(db: AsyncSession, mobile_number: str):
    result = await db.execute(select(User).where(User.mobile_number == mobile_number))
    return result.scalar_one_or_none()


async def get_user_role(db, user_id: int):
    result = await db.execute(
        select(Role.role_name)
        .join(UserRole, Role.role_id == UserRole.role_id)
        .where(UserRole.user_id == user_id)
    )
    return result.scalar_one_or_none()
