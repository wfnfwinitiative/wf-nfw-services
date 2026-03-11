from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OpportunityBaseSchema(BaseModel):
    class Config:
        from_attributes = True


class OpportunityCreate(BaseModel):
    donor_id: int
    hunger_spot_id: int
    status_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    feeding_count: Optional[int] = 0
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None


class OpportunityRead(OpportunityBaseSchema):
    opportunity_id: int
    donor_id: int
    status_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    creator_id: int
    feeding_count: Optional[int]
    pickup_eta: Optional[datetime]
    delivery_by: Optional[datetime]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    notes: Optional[str]
    image_link: Optional[str]
    created_at: datetime
    updated_at: datetime

class OpportunityUpdate(BaseModel):
    donor_id: int
    status_id: int
    creator_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    feeding_count: Optional[int] = 0
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None
    start_time: Optional[datetime]
    end_time: Optional[datetime]

class OpportunityDetailedRead(OpportunityBaseSchema):
    opportunity_id: int
    opportunity_name: str
    donor_id: int
    donor_name: str
    status_id: int
    status_name: str
    driver_id: Optional[int]
    driver_name: Optional[str]
    vehicle_id: Optional[int]
    vehicle_name: Optional[str]
    creator_id: int
    creator_name: str
    feeding_count: Optional[int]
    pickup_eta: Optional[datetime]
    delivery_by: Optional[datetime]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    notes: Optional[str]
    image_link: Optional[str]
    pickup_location: Optional[str]
    pickup_contact_no: Optional[str]
    drop_location: Optional[str]
    drop_location_contact_no: Optional[str]
    created_at: datetime
    updated_at: datetime