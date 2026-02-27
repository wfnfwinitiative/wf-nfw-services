from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class OpportunityEvent(Base):
    __tablename__ = "opportunity_events"
    __table_args__ = {"schema": SCHEMA}

    opportunity_event_id = Column(BigInteger, Identity(), primary_key=True)
    opportunity_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"), nullable=False)

    event_type = Column(String(50), nullable=False)

    previous_status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"))
    new_status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"))

    event_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    actor_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))
    notes = Column(Text)