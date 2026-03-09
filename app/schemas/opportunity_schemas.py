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
    creator_id: Optional[int] = None
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    feeding_count: Optional[int] = 0
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None


class OpportunityRead(OpportunityBaseSchema):
    opportunity_id: int
    donor_id: int
    hunger_spot_id: int
    status_id: int
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    creator_id: int
    assignee_id: Optional[int] = None
    feeding_count: Optional[int] = None
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class OpportunityUpdate(BaseModel):
    donor_id: int
    status_id: int
    creator_id: int
    driver_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    feeding_count: Optional[int] = 0
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
