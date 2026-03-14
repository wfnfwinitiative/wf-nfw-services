from sqlalchemy import Column, BigInteger, SmallInteger, ForeignKey
from app.db.session import Base
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(
        BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), primary_key=True
    )
    role_id = Column(
        SmallInteger, ForeignKey(f"{SCHEMA}.roles.role_id"), primary_key=True
    )
