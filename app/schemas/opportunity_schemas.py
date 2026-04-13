from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.opportunity_item_schemas import OpportunityItemRead


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
    hunger_spot_id: Optional[int]
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
    pickup_folder_id: Optional[str]
    delivery_folder_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    previous_status_id: Optional[int]
    new_status_id: Optional[int]

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
    pickup_folder_id: Optional[str]
    delivery_folder_id: Optional[str]
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
    pickup_folder_id: Optional[str]
    delivery_folder_id: Optional[str]
    pickup_location: Optional[str]
    pickup_contact_no: Optional[str]
    pickup_lat: Optional[float]
    pickup_lng: Optional[float]
    drop_location: Optional[str]
    drop_location_contact_no: Optional[str]
    drop_lat: Optional[float]
    drop_lng: Optional[float]
    created_at: datetime
    updated_at: datetime
    previous_status_id: Optional[int]
    new_status_id: Optional[int]


class OpportunityTrackingRead(OpportunityBaseSchema):
    opportunity_id: int
    donor_id: int
    status_id: int
    status_name: str
    driver_id: Optional[int]
    driver_name: Optional[str]
    vehicle_id: Optional[int]
    vehicle_name: Optional[str]
    creator_id: int
    creator_name: str
    donor_name: str
    hunger_spot_name: Optional[str]
    pickup_location: Optional[str]
    pickup_lat: Optional[float]
    pickup_lng: Optional[float]
    drop_location: Optional[str]
    drop_lat: Optional[float]
    drop_lng: Optional[float]
    pickup_eta: Optional[datetime]
    delivery_by: Optional[datetime]
    previous_status_id: Optional[int]
    previous_status_name: Optional[str]
    new_status_id: Optional[int]
    new_status_name: Optional[str]


class OpportunityDetailRead(OpportunityBaseSchema):
    opportunity_id: int
    donor_id: int
    hunger_spot_id: int
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
    pickup_folder_id: Optional[str]
    delivery_folder_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    opportunity_items: list[OpportunityItemRead]
    previous_status_id: Optional[int]
    new_status_id: Optional[int]