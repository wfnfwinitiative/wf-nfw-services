from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    Numeric,
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class HungerSpot(Base):
    __tablename__ = "hunger_spots"
    __table_args__ = {"schema": SCHEMA}

    hunger_spot_id = Column(BigInteger, Identity(), primary_key=True)
    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)

    spot_name = Column(String(100), nullable=False)
    city = Column(String(100))
    pincode = Column(String(10))
    contact_person = Column(String(100))
    mobile_number = Column(String(15))
    address = Column(String(255))
    location = Column(String(255))
    capacity_meals = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
