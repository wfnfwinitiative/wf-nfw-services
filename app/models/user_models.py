from sqlalchemy import Column, BigInteger, String, Boolean, TIMESTAMP
from sqlalchemy.schema import Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(BigInteger, Identity(), primary_key=True)
    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    roles = relationship(
        "Role",
        secondary=f"{SCHEMA}.user_roles",
        back_populates="users",
        lazy="selectin"
    )