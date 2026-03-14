from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from typing import List
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Returns full JWT payload including user_id and role."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        role = payload.get("role")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": int(user_id), "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_roles(allowed_roles: List[str]):
    """Dependency factory that restricts access to specific roles.

    Usage:
        caller: dict = Depends(require_roles(["ADMIN"]))
        caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR"]))
        caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR", "DRIVER"]))
    """

    def role_checker(caller: dict = Depends(get_current_user_payload)):
        # user roles is a list.
        user_roles = caller.get("role") or []
        user_roles = user_roles if isinstance(user_roles, list) else [user_roles]
        print(user_roles)
        print(allowed_roles)
        print(any(r in allowed_roles for r in user_roles))
        if not any(r in allowed_roles for r in user_roles):
            print("Did it reach here ??")
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}",
            )
        return caller

    return role_checker
