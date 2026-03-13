import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
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
    text
)
from sqlalchemy.schema import Identity
from sqlalchemy.sql import func

from app.db.session import engine, Base
from app.core.config import settings

# ==========================
# DATABASE CONFIG
# ==========================
SCHEMA = settings.DB_SCHEMA

# ==========================
# MASTER TABLES
# ==========================

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(BigInteger, Identity(), primary_key=True)
    name = Column(String, nullable=False)
    password_hash = Column(String(255), nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": SCHEMA}

    role_id = Column(SmallInteger, Identity(), primary_key=True)
    role_name = Column(String, unique=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": SCHEMA}

    user_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), primary_key=True)
    role_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.roles.role_id"), primary_key=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Vehicle(Base):
    __tablename__ = "vehicles"
    __table_args__ = {"schema": SCHEMA}

    vehicle_id = Column(BigInteger, Identity(), primary_key=True)
    vehicle_no = Column(String, unique=True, nullable=False)
    notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Donor(Base):
    __tablename__ = "donors"
    __table_args__ = {"schema": SCHEMA}

    donor_id = Column(BigInteger, Identity(), primary_key=True)
    donor_name = Column(String, nullable=False)
    city = Column(String)
    pincode = Column(String)
    contact_person = Column(String)
    mobile_number = Column(String)
    address = Column(String)
    location = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class HungerSpot(Base):
    __tablename__ = "hunger_spots"
    __table_args__ = {"schema": SCHEMA}

    hunger_spot_id = Column(BigInteger, Identity(), primary_key=True)
    spot_name = Column(String, nullable=False)
    city = Column(String)
    pincode = Column(String)
    contact_person = Column(String)
    mobile_number = Column(String)
    address = Column(String)
    location = Column(String)
    capacity_meals = Column(Integer)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Status(Base):
    __tablename__ = "statuses"
    __table_args__ = {"schema": SCHEMA}

    status_id = Column(SmallInteger, Identity(), primary_key=True)
    status_name = Column(String, unique=True, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# ==========================
# CORE WORKFLOW TABLES
# ==========================

class Opportunity(Base):
    __tablename__ = "opportunities"
    __table_args__ = {"schema": SCHEMA}

    opportunity_id = Column(BigInteger, Identity(), primary_key=True)

    donor_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.donors.donor_id"), nullable=False)
    status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"), nullable=False)

    driver_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))
    vehicle_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.vehicles.vehicle_id"))

    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"), nullable=False)
    assignee_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))

    feeding_count = Column(Integer)
    pickup_eta = Column(TIMESTAMP(timezone=True))
    delivery_by = Column(TIMESTAMP(timezone=True))
    start_time = Column(TIMESTAMP(timezone=True))
    end_time = Column(TIMESTAMP(timezone=True))

    notes = Column(Text)
    image_link = Column(String)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class OpportunityItem(Base):
    __tablename__ = "opportunity_items"
    __table_args__ = {"schema": SCHEMA}

    opportunity_item_id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"), nullable=False)

    food_name = Column(String, nullable=False)
    quality = Column(String)
    quantity_value = Column(Numeric(10, 2), nullable=False)
    quantity_unit = Column(String, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class OpportunityAllocation(Base):
    __tablename__ = "opportunity_allocations"
    __table_args__ = {"schema": SCHEMA}

    opportunity_allocation_id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_item_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunity_items.opportunity_item_id"),
                                 nullable=False)
    hunger_spot_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.hunger_spots.hunger_spot_id"), nullable=False)

    allocated_value = Column(Numeric(10, 2), nullable=False)
    allocated_unit = Column(String, nullable=False)

    notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class OpportunityEvent(Base):
    __tablename__ = "opportunity_events"
    __table_args__ = {"schema": SCHEMA}

    opportunity_event_id = Column(BigInteger, Identity(), primary_key=True)

    opportunity_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.opportunities.opportunity_id"), nullable=False)

    previous_status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"))
    new_status_id = Column(SmallInteger, ForeignKey(f"{SCHEMA}.statuses.status_id"))

    event_time = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    creator_id = Column(BigInteger, ForeignKey(f"{SCHEMA}.users.user_id"))
    notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# ==========================
# RECREATE TABLES
# ==========================

async def recreate_tables():
    async with AsyncSession(engine) as conn:
        await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}"))

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

        # Seed statuses
        await conn.execute(text(f"""
            INSERT INTO {SCHEMA}.statuses (status_name)
            VALUES
            ('Initiated'),
            ('UnderReview'),
            ('Approved'),
            ('Assigned'),
            ('InPickup'),
            ('InTransit'),
            ('Delivered'),
            ('Verified'),
            ('Closed'),
            ('Rejected'),
            ('Cancelled')
            ON CONFLICT (status_name) DO NOTHING;
        """))

    print("✅ All tables dropped, recreated and seeded successfully!")


if __name__ == "__main__":
    asyncio.run(recreate_tables())