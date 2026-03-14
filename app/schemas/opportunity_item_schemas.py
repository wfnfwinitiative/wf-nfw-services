from pydantic import BaseModel
from decimal import Decimal
from typing import Optional


class OpportunityItemBase(BaseModel):
    class Config:
        from_attributes = True


class OpportunityItemCreate(BaseModel):
    opportunity_id: int
    food_name: str
    quality: Optional[str] = None
    quantity_value: Decimal
    quantity_unit: str


class OpportunityItemRead(OpportunityItemBase):
    opportunity_item_id: int
    opportunity_id: int
    food_name: str
    quality: Optional[str]
    quantity_value: Decimal
    quantity_unit: str


class OpportunityItemUpdate(BaseModel):
    opportunity_id: int
    food_name: str
    quality: Optional[str] = None
    quantity_value: Decimal
    quantity_unit: str
