from sqlalchemy import (
    Column, BigInteger, SmallInteger, Integer,
    String, Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

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

    feeding_count = Column(Integer)
    pickup_eta = Column(TIMESTAMP(timezone=True))
    delivery_by = Column(TIMESTAMP(timezone=True))
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))

    notes = Column(Text)
    image_link = Column(String(255))

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)