from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import hashlib
from app.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def _pre_hash(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    return pwd_context.hash(_pre_hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_pre_hash(plain_password), hashed_password)


def create_access_token(user_id: int, role: str):
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
