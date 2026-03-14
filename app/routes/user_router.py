from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user_schemas import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService
from app.dependencies.auth import get_current_user_payload, require_roles

router = APIRouter(prefix="/users", tags=["Users"])


class AdminPasswordReset(BaseModel):
    mobile_number: str
    new_password: str = Field(min_length=8)


class ChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)


@router.post("/", response_model=UserRead)
async def create_user_with_role(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "SUPPORTADMIN"])),
):
    return await UserService(db).create_user_with_role(
        name=payload.name,
        mobile_number=payload.mobile_number,
        password=payload.password,
        role_name=payload.role_name,
        email=payload.email,
        caller=caller,
    )


@router.post("/reset-admin-password")
async def reset_admin_password(
    payload: AdminPasswordReset,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["SUPPORTADMIN"])),
):
    return await UserService(db).reset_admin_password(
        mobile_number=payload.mobile_number,
        new_password=payload.new_password,
        caller=caller,
    )


@router.post("/change-password")
async def change_password(
    payload: ChangePassword,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "COORDINATOR", "DRIVER"])),
):
    return await UserService(db).change_password(
        current_password=payload.current_password,
        new_password=payload.new_password,
        caller=caller,
    )


@router.post("/unlock/{user_id}")
async def unlock_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "SUPPORTADMIN"])),
):
    return await UserService(db).unlock_user(
        user_id=user_id,
        caller=caller,
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(get_current_user_payload),
):
    return await UserService(db).get_user(user_id)


@router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_all_users()


@router.get("/by-role/{role_name}", response_model=list[UserRead])
async def get_users_by_role(role_name: str, db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_users_by_role(role_name)


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN"])),
):
    return await UserService(db).update_user(
        user_id,
        **payload.dict(exclude_unset=True),
    )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN"])),
):
    if caller.get("user_id") == user_id:
        raise HTTPException(
            status_code=400, detail="Logged-in User Cannot be deactivated"
        )
    return await UserService(db).deactivate_user(user_id)


@router.post("/activate/{user_id}")
async def activate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    caller: dict = Depends(require_roles(["ADMIN", "SUPPORTADMIN"])),
):
    return await UserService(db).activate_user(user_id)
