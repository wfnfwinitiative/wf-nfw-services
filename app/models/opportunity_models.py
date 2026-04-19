from sqlalchemy import (
    Column, BigInteger, SmallInteger, Integer, Numeric,
    String, Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

# Importing the Status model ensures it is registered in metadata
# before Opportunity defines a ForeignKey to it.
from app.models.status_models import Status  # noqa: F401

SCHEMA = settings.DB_SCHEMA


class Opportunity(Base):
    __tablename__ = "opportunities"
    __table_args__ = {"schema": SCHEMA}

    opportunity_id = Column(BigInteger, Identity(), primary_key=True)

    donor_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.donors.donor_id"), nullable=False)
    hunger_spot_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.hunger_spots.hunger_spot_id"))
    status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"), nullable=False)

    driver_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))
    vehicle_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.vehicles.vehicle_id"))

    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))

    estimated_count = Column(Integer)
    estimated_unit = Column(String(10))

    feeding_count = Column(Integer)
    food_collected = Column(Numeric(10, 2))

    pickup_eta = Column(TIMESTAMP(timezone=True))
    delivery_by = Column(TIMESTAMP(timezone=True))
    picked_up_at = Column(TIMESTAMP(timezone=True))
    delivered_at = Column(TIMESTAMP(timezone=True))

    notes = Column(Text)
    image_link = Column(String(255))

    pickup_folder_id = Column(String(255))
    delivery_folder_id = Column(String(255))

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)