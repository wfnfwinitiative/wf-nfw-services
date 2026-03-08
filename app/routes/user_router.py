from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user_schemas import UserCreate, UserRead
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead)
async def create_user_with_role(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).create_user_with_role(
        name=payload.name,
        mobile_number=payload.mobile_number,
        password=payload.password,
        role_name=payload.role_name
    )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_user(user_id)


@router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_all_users()


@router.patch("/{user_id}")
async def deactivate_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService(db).deactivate_user(user_id)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await UserService(db).deactivate_user(user_id)