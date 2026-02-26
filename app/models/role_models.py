from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.schema import Identity
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}

    role_id = Column(SmallInteger, Identity(), primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)