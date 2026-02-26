from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DonorBaseSchema(BaseModel):
    class Config:
        from_attributes = True


class DonorCreate(BaseModel):
    donor_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None


class DonorRead(DonorBaseSchema):
    donor_id: int
    donor_name: str
    city: Optional[str]
    pincode: Optional[str]
    contact_person: Optional[str]
    mobile_number: Optional[str]
    address: Optional[str]
    location: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

class DonorUpdate(BaseModel):
    donor_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None