from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user_login_schemas import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db=db)

    token = await auth_service.authenticate_user(
        mobile=data.mobile_number, password=data.password
    )

    return {"access_token": token, "token_type": "bearer"}