from sqlalchemy import Column, BigInteger, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": SCHEMA}

    vehicle_id = Column(BigInteger, Identity(), primary_key=True)
    vehicle_no = Column(String(20), unique=True, nullable=False)
    notes = Column(Text)
    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)