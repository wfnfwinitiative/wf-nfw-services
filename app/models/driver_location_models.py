from sqlalchemy import Column, BigInteger, Float, TIMESTAMP, ForeignKey
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class DriverLocation(Base):
    __tablename__ = "driver_locations"
    __table_args__ = {"schema": SCHEMA}

    id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"),
        nullable=False,
        unique=True,
        index=True,
    )
    driver_id = Column(
        BigInteger,
        ForeignKey(f"{SCHEMA}.users.user_id"),
        nullable=False,
    )

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=True)

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
