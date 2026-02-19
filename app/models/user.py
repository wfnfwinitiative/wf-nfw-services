from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    name: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    phone: Optional[str] = None
    name: Optional[str] = None
    active: Optional[str] = None


class UserRead(UserBase):
    id: UUID
    active: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
