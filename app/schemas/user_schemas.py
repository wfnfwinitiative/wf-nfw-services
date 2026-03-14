from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    mobile_number: str
    password: str = Field(min_length=8)
    role_name: str
    email: Optional[str] = None


class UserRead(BaseModel):
    user_id: int
    name: str
    mobile_number: str
    email: Optional[str] = None
    is_active: bool
    created_at: datetime
    roles: list[str] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    mobile_number: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
