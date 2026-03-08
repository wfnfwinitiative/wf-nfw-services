from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    mobile_number: str
    password: str = Field(min_length=8)
    role_name: str


class UserRead(BaseModel):
    user_id: int
    name: str
    mobile_number: str
    is_active: bool
    created_at: datetime
    roles: list[str] = []

    class Config:
        from_attributes = True