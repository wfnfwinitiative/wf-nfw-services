from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class OpportunityAllocationBase(BaseModel):
    class Config:
        from_attributes = True


class OpportunityAllocationCreate(BaseModel):
    opportunity_item_id: int
    hunger_spot_id: int
    allocated_value: Decimal
    allocated_unit: str
    notes: Optional[str] = None


class OpportunityAllocationRead(OpportunityAllocationBase):
    opportunity_allocation_id: int
    opportunity_item_id: int
    hunger_spot_id: int
    allocated_value: Decimal
    allocated_unit: str
    notes: Optional[str]

class OpportunityAllocationUpdate(BaseModel):
    opportunity_item_id: int
    hunger_spot_id: int
    allocated_value: Decimal
    allocated_unit: str
    notes: Optional[str] = None