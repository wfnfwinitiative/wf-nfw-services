from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OpportunityEventBase(BaseModel):
    class Config:
        from_attributes = True


class OpportunityEventCreate(BaseModel):
    opportunity_id: int
    previous_status_id: Optional[int] = None
    new_status_id: Optional[int] = None
    creator_id: Optional[int] = None
    notes: Optional[str] = None


class OpportunityEventRead(OpportunityEventBase):
    opportunity_event_id: int
    opportunity_id: int
    previous_status_id: Optional[int]
    new_status_id: Optional[int]
    event_time: datetime
    creator_id: Optional[int]
    notes: Optional[str]