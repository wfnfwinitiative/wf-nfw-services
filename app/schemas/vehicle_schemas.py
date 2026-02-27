from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehicleBaseSchema(BaseModel):
    class Config:
        from_attributes = True


class VehicleCreate(BaseModel):
    vehicle_no: str
    notes: Optional[str] = None


class VehicleRead(VehicleBaseSchema):
    vehicle_id: int
    vehicle_no: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

class VehicleUpdate(BaseModel):
    vehicle_no: str
