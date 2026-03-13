from sqlalchemy import Column, SmallInteger, String, TIMESTAMP
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func

from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class Status(Base):
    __tablename__ = "statuses"
    __table_args__ = {"schema": SCHEMA}

    status_id = Column(SmallInteger, Identity(), primary_key=True)
    status_name = Column(String, unique=True, nullable=False)
    status_info = Column(String, nullable=False)
