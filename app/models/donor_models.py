from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.core.config import settings

from app.db.session import Base
SCHEMA = settings.DB_SCHEMA


class Donor(Base):
    __tablename__ = "donors"
    __table_args__ = {"schema": SCHEMA}

    donor_id = Column(BigInteger, Identity(), primary_key=True)
    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)

    donor_name = Column(String(100), nullable=False)
    city = Column(String(100))
    pincode = Column(String(10))
    contact_person = Column(String(100))
    mobile_number = Column(String(15))
    address = Column(String(255))
    location = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)