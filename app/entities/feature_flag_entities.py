from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    Text,
    TIMESTAMP,
    ForeignKey,
    Index,
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from app.core.config import settings

Base = declarative_base()
SCHEMA = settings.DB_SCHEMA


# ==============================
# FEATURE FLAGS
# ==============================

class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    __table_args__ = (
        Index("idx_feature_flag_name", "feature_flag_name"),
        {"schema": SCHEMA},
    )

    id = Column(BigInteger, Identity(), primary_key=True)
    feature_flag_name = Column(String(100), unique=True, nullable=False)
    enabled = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
