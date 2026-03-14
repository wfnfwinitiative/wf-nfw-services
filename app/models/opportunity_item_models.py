from sqlalchemy import Column, BigInteger, String, Numeric, ForeignKey
from sqlalchemy.schema import Identity
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class OpportunityItem(Base):
    __tablename__ = "opportunity_items"
    __table_args__ = {"schema": SCHEMA}

    opportunity_item_id = Column(BigInteger, Identity(), primary_key=True)
    opportunity_id = Column(
        BigInteger, ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"), nullable=False
    )

    food_name = Column(String(100), nullable=False)
    quality = Column(String(100))
    quantity_value = Column(Numeric(10, 2), nullable=False)
    quantity_unit = Column(String(20), nullable=False)
