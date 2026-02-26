from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


# =====================================================
# BASE CONFIG
# =====================================================

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True  # Pydantic v2 compatible


# =====================================================
# AUTH
# =====================================================

class LoginRequest(BaseModel):
    mobile_number: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =====================================================
# USERS
# =====================================================

class AdminCreateUser(BaseModel):
    name: str
    mobile_number: str
    password: str = Field(min_length=8)
    role: str  # ADMIN / COORDINATOR / DRIVER


class UserRead(BaseSchema):
    user_id: int
    name: str
    mobile_number: str
    is_active: bool
    created_at: datetime


# =====================================================
# ROLES
# =====================================================

class RoleRead(BaseSchema):
    role_id: int
    role_name: str


# =====================================================
# VEHICLES
# =====================================================

class VehicleCreate(BaseModel):
    vehicle_no: str
    notes: Optional[str] = None


class VehicleRead(BaseSchema):
    vehicle_id: int
    vehicle_no: str
    notes: Optional[str]
    created_at: datetime


# =====================================================
# DONORS
# =====================================================

class DonorCreate(BaseModel):
    donor_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None


class DonorRead(BaseSchema):
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


# =====================================================
# HUNGER SPOTS
# =====================================================

class HungerSpotCreate(BaseModel):
    spot_name: str
    city: Optional[str] = None
    pincode: Optional[str] = None
    contact_person: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    capacity_meals: Optional[int] = None


class HungerSpotRead(BaseSchema):
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


# =====================================================
# STATUS
# =====================================================

class StatusRead(BaseSchema):
    status_id: int
    status_name: str


# =====================================================
# OPPORTUNITY ITEMS
# =====================================================

class OpportunityItemCreate(BaseModel):
    food_name: str
    quality: Optional[str] = None
    quantity_value: Decimal
    quantity_unit: str


class OpportunityItemRead(BaseSchema):
    opportunity_item_id: int
    food_name: str
    quality: Optional[str]
    quantity_value: Decimal
    quantity_unit: str


# =====================================================
# OPPORTUNITY ALLOCATIONS
# =====================================================

class OpportunityAllocationCreate(BaseModel):
    opportunity_item_id: int
    hunger_spot_id: int
    allocated_value: Decimal
    allocated_unit: str
    notes: Optional[str] = None


class OpportunityAllocationRead(BaseSchema):
    opportunity_allocation_id: int
    opportunity_item_id: int
    hunger_spot_id: int
    allocated_value: Decimal
    allocated_unit: str
    notes: Optional[str]


# =====================================================
# OPPORTUNITY EVENTS
# =====================================================

class OpportunityEventCreate(BaseModel):
    opportunity_id: int
    event_type: str
    previous_status_id: Optional[int] = None
    new_status_id: Optional[int] = None
    notes: Optional[str] = None


class OpportunityEventRead(BaseSchema):
    opportunity_event_id: int
    opportunity_id: int
    event_type: str
    previous_status_id: Optional[int]
    new_status_id: Optional[int]
    event_time: datetime
    actor_id: Optional[int]
    notes: Optional[str]


# =====================================================
# OPPORTUNITY
# =====================================================

class OpportunityCreate(BaseModel):
    donor_id: int
    status_id: int
    creator_id: int
    feeding_count: Optional[int] = 0
    pickup_eta: Optional[datetime] = None
    delivery_by: Optional[datetime] = None
    notes: Optional[str] = None
    image_link: Optional[str] = None


class OpportunityRead(BaseSchema):
    opportunity_id: int
    donor_id: int
    status_id: int
    driver_id: Optional[int]
    vehicle_id: Optional[int]
    creator_id: int
    assignee_id: Optional[int]
    feeding_count: Optional[int]
    pickup_eta: Optional[datetime]
    delivery_by: Optional[datetime]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    notes: Optional[str]
    image_link: Optional[str]
    created_at: datetime
    updated_at: datetime


# =====================================================
# NESTED OPPORTUNITY VIEW (for frontend detail screen)
# =====================================================

class OpportunityDetailRead(OpportunityRead):
    items: List[OpportunityItemRead] = []
    events: List[OpportunityEventRead] = []