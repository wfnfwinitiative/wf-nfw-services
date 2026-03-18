from sqlalchemy import Column, BigInteger, SmallInteger, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class DriverLocation(Base):
    """Stores the latest known GPS location for a driver on an active opportunity.
    One row per opportunity — upserted on each update from the driver."""

    __tablename__ = "driver_locations"
    __table_args__ = {"schema": SCHEMA}

    location_id = Column(BigInteger, Identity(), primary_key=True)
    opportunity_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"),
        nullable=False,
        unique=True,  # one live row per opportunity
        index=True,
    )
    driver_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)
    latitude = Column(Numeric(10, 7), nullable=False)
    longitude = Column(Numeric(10, 7), nullable=False)
    accuracy = Column(Numeric(10, 2))          # metres, from browser Geolocation API
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
