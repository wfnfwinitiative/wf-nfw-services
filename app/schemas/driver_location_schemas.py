from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DriverLocationUpdate(BaseModel):
    """Sent by the driver's browser every polling interval."""
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    accuracy: Optional[float] = Field(None, ge=0)


class DriverLocationRead(BaseModel):
    opportunity_id: int
    driver_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float]
    updated_at: datetime

    class Config:
        from_attributes = True
