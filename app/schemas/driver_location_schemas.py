from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DriverLocationUpsert(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    accuracy: Optional[float] = Field(None, ge=0)


class DriverLocationRead(BaseModel):
    class Config:
        from_attributes = True

    opportunity_id: int
    driver_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float]
    updated_at: datetime
