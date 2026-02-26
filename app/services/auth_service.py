from fastapi import HTTPException
from app.db.db_read import get_user_by_mobile, get_user_role
from app.core.security import verify_password, create_access_token


async def authenticate_user(db, mobile: str, password: str):

    # 1️⃣ Fetch user
    user = await get_user_by_mobile(db, mobile)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2️⃣ Verify password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3️⃣ Fetch role
    role_name = await get_user_role(db, user.user_id)
    if not role_name:
        raise HTTPException(status_code=403, detail="User has no assigned role")

    # 4️⃣ Create token with role
    token = create_access_token(user_id=user.user_id, role=role_name)

    return token
