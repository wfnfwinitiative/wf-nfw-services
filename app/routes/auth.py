from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import LoginRequest
from app.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):

    token = await authenticate_user(
        db, mobile=data.mobile_number, password=data.password
    )

    return {"access_token": token, "token_type": "bearer"}
