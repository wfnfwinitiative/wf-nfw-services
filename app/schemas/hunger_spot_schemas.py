from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HungerSpotBaseSchema(BaseModel):
    class Config:
        from_attributes = True


class HungerSpotCreate(BaseModel):
    spot_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    capacity_meals: Optional[int] = None


class HungerSpotRead(HungerSpotBaseSchema):
    hunger_spot_id: int
    spot_name: str
    city: Optional[str]
    pincode: Optional[str]
    contact_person: Optional[str]
    mobile_number: Optional[str]
    address: Optional[str]
    location: Optional[str]
    capacity_meals: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class HungerSpotUpdate(BaseModel):
    spot_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    capacity_meals: Optional[int] = None