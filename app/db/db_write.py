from sqlalchemy.ext.asyncio import AsyncSession
from app.entities.entities import User, UserRole


async def create_user_record(
    db: AsyncSession, name: str, mobile: str, password_hash: str
):
    user = User(name=name, mobile_number=mobile, password_hash=password_hash)
    db.add(user)
    await db.flush()
    return user


async def assign_role_to_user(db: AsyncSession, user_id: int, role_id: int):
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
