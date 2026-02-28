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
    creator_id: int
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
