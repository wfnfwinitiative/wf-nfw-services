from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.db.db_read import get_role_by_name
from app.db.db_write import create_user_record, assign_role_to_user
from app.core.security import hash_password


async def create_user_with_role(
    db: AsyncSession, name: str, mobile: str, password: str, role_name: str
):

    # Validate role
    role = await get_role_by_name(db, role_name)
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Hash password
    hashed = hash_password(password)

    # Create user
    user = await create_user_record(db, name, mobile, hashed)

    # Assign role
    await assign_role_to_user(db, user.user_id, role.role_id)

    await db.commit()

    return user
