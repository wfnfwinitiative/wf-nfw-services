from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import UserRead, UserCreate, UserUpdate
from app.services.user_service import UserService
from app.database import get_db
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)


@router.get("/", response_model=List[UserRead])
async def list_users(service: UserService = Depends(get_user_service)):
    users = await service.list_users()
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    existing = await service.repo.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = await service.create_user(payload)
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, payload: UserUpdate, service: UserService = Depends(get_user_service)):
    user = await service.update_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    ok = await service.delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
