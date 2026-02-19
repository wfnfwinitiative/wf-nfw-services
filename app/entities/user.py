from sqlalchemy import Column, String, CHAR, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.database import Base
import uuid
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "wfnfw"}

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True)
    name = Column(String)
    active = Column(CHAR(1), default="Y")
    created_at = Column(DateTime, default=datetime.utcnow)
