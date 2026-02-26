from sqlalchemy import Column, BigInteger, String, Numeric, Text, ForeignKey
from sqlalchemy.schema import Identity
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class OpportunityAllocation(Base):
    __tablename__ = "opportunity_allocations"
    __table_args__ = {"schema": SCHEMA}

    opportunity_allocation_id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_item_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunity_items.opportunity_item_id"), nullable=False)
    hunger_spot_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.hunger_spots.hunger_spot_id"), nullable=False)

    allocated_value = Column(Numeric(10, 2), nullable=False)
    allocated_unit = Column(String(20), nullable=False)
    notes = Column(Text)