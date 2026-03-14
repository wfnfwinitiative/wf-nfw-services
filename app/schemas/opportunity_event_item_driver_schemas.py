from pydantic import BaseModel
from typing import List


from app.schemas.opportunity_event_schema import (
    OpportunityEventCreate,
    OpportunityEventRead,
)
from app.schemas.opportunity_item_schemas import (
    OpportunityItemRead,
    OpportunityItemCreate,
)


class OpportunityEventItemDriverRead(BaseModel):
    event: OpportunityEventRead
    items: List[OpportunityItemRead]

    class Config:
        from_attributes = True


class OpportunityEventItemDriverCreate(BaseModel):
    event_data: OpportunityEventCreate
    items_data: List[OpportunityItemCreate]
