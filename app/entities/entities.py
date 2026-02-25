from sqlalchemy import (
    Column,
    BigInteger,
    SmallInteger,
    Integer,
    String,
    Boolean,
    Text,
    TIMESTAMP,
    ForeignKey,
    Numeric,
    Index,
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from app.core.config import settings

Base = declarative_base()
SCHEMA = settings.DB_SCHEMA


# ==============================
# USERS
# ==============================

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_user_mobile", "mobile_number"),
        {"schema": SCHEMA},
    )

    user_id = Column(BigInteger, Identity(), primary_key=True)
    name = Column(String(100), nullable=False)
    mobile_number = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    roles = relationship("UserRole", back_populates="user")


# ==============================
# ROLES
# ==============================

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}

    role_id = Column(SmallInteger, Identity(), primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)

    users = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), primary_key=True)
    role_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.roles.role_id"), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


# ==============================
# MASTER TABLES
# ==============================

class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": SCHEMA}

    vehicle_id = Column(BigInteger, Identity(), primary_key=True)
    vehicle_no = Column(String(20), unique=True, nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class Donor(Base):
    __tablename__ = "donors"
    __table_args__ = {"schema": SCHEMA}

    donor_id = Column(BigInteger, Identity(), primary_key=True)
    donor_name = Column(String(100), nullable=False)
    city = Column(String(100))
    pincode = Column(String(10))
    contact_person = Column(String(100))
    mobile_number = Column(String(15))
    address = Column(String(255))
    location = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class HungerSpot(Base):
    __tablename__ = "hunger_spots"
    __table_args__ = {"schema": SCHEMA}

    hunger_spot_id = Column(BigInteger, Identity(), primary_key=True)
    spot_name = Column(String(100), nullable=False)
    city = Column(String(100))
    pincode = Column(String(10))
    contact_person = Column(String(100))
    mobile_number = Column(String(15))
    address = Column(String(255))
    location = Column(String(255))
    capacity_meals = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class Status(Base):
    __tablename__ = "statuses"
    __table_args__ = {"schema": SCHEMA}

    status_id = Column(SmallInteger, Identity(), primary_key=True)
    status_name = Column(String(50), unique=True, nullable=False)


# ==============================
# OPPORTUNITIES
# ==============================

class Opportunity(Base):
    __tablename__ = "opportunities"
    __table_args__ = (
        Index("idx_opportunity_status", "status_id"),
        Index("idx_opportunity_donor", "donor_id"),
        {"schema": SCHEMA},
    )

    opportunity_id = Column(BigInteger, Identity(), primary_key=True)

    donor_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.donors.donor_id"), nullable=False)
    status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"), nullable=False)

    driver_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))
    vehicle_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.vehicles.vehicle_id"))

    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))

    feeding_count = Column(Integer)
    pickup_eta = Column(TIMESTAMP)
    delivery_by = Column(TIMESTAMP)
    start_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)

    notes = Column(Text)
    image_link = Column(String(255))

    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    items = relationship("OpportunityItem", back_populates="opportunity")
    events = relationship("OpportunityEvent", back_populates="opportunity")


class OpportunityItem(Base):
    __tablename__ = "opportunity_items"
    __table_args__ = {"schema": SCHEMA}

    opportunity_item_id = Column(BigInteger, Identity(), primary_key=True)
    opportunity_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"), nullable=False)

    food_name = Column(String(100), nullable=False)
    quality = Column(String(100))
    quantity_value = Column(Numeric(10, 2), nullable=False)
    quantity_unit = Column(String(20), nullable=False)

    opportunity = relationship("Opportunity", back_populates="items")
    allocations = relationship("OpportunityAllocation", back_populates="item")


class OpportunityAllocation(Base):
    __tablename__ = "opportunity_allocations"
    __table_args__ = {"schema": SCHEMA}

    opportunity_allocation_id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_item_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunity_items.opportunity_item_id"), nullable=False)
    hunger_spot_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.hunger_spots.hunger_spot_id"), nullable=False)

    allocated_value = Column(Numeric(10, 2), nullable=False)
    allocated_unit = Column(String(20), nullable=False)
    notes = Column(Text)

    item = relationship("OpportunityItem", back_populates="allocations")


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

    opportunity = relationship("Opportunity", back_populates="events")