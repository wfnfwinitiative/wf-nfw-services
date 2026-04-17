"""
Seed script to populate test data:
- SEED_COUNT Users (mix of roles)
- SEED_COUNT Donors (Hyderabad-based)
- SEED_COUNT Hunger Spots (Hyderabad-based)
- SEED_COUNT Vehicles (unique license plates)
"""

import asyncio
import random
import string
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import engine
from app.models.user_models import User
from app.models.role_models import Role
from app.models.user_role_models import UserRole
from app.models.donor_models import Donor
from app.models.hunger_spot_models import HungerSpot
from app.models.vehicle_models import Vehicle
from app.core.security import hash_password
from app.core.config import settings

SCHEMA = settings.DB_SCHEMA

# Hyderabad locations and areas with REAL GPS coordinates
HYDERABAD_AREAS_WITH_COORDS = {
    "Jubilee Hills": (17.4201, 78.4446),
    "Banjara Hills": (17.4239, 78.4352),
    "Filmnagar": (17.4243, 78.4482),
    "Gachibowli": (17.4407, 78.4457),
    "Manikonda": (17.4291, 78.3829),
    "Kondapur": (17.4669, 78.3573),
    "Mindspace": (17.4432, 78.4546),
    "Hitech City": (17.4439, 78.4284),
    "Inorbit": (17.4480, 78.4432),
    "Whitefield": (17.4520, 78.4285),
    "Kukatpally": (17.4950, 78.4255),
    "Yousufguda": (17.3821, 78.4671),
    "Madhapur": (17.4589, 78.4518),
    "Tellapur": (17.5219, 78.4346),
    "JNTU": (17.5050, 78.4826),
    "Ameerpet": (17.3798, 78.4651),
    "Secunderabad": (17.3676, 78.5036),
    "Lakdi-ka-Pool": (17.3565, 78.4758),
    "Charminar": (17.3639, 78.4740),
    "Abids": (17.3750, 78.4695),
    "Hyderabad Fort": (17.3713, 78.4766),
    "Osman Nagar": (17.3947, 78.5156),
    "Tarnaka": (17.4294, 78.5341),
    "Begumpet": (17.3873, 78.4636),
    "Somajiguda": (17.3924, 78.4556),
    "Nampally": (17.3731, 78.4745),
    "Tank Bund": (17.3825, 78.4681),
    "Punjagutta": (17.3912, 78.4626),
    "Panjagutta": (17.3912, 78.4626),
    "Iqbal Pur": (17.3654, 78.4872),
}

# For backward compatibility, keep the list of area names
HYDERABAD_AREAS = list(HYDERABAD_AREAS_WITH_COORDS.keys())

# Hyderabad address patterns
ADDRESS_PATTERNS = [
    "Plot {num}, {area}, Hyderabad{pin}",
    "{num}-{letter} {area}, Hyderabad{pin}",
    "{name} Building, {area}, Hyderabad{pin}",
    "{num}/A {area}, Hyderabad{pin}",
    "Street {letter}, {area}, Hyderabad{pin}",
    "{name} Complex, {area}, Hyderabad{pin}",
    "{num} Main Road, {area}, Hyderabad{pin}",
    "Lane {num}, {area}, Hyderabad{pin}",
]

# Building/organization names
BUILDING_NAMES = [
    "Galaxy", "Crown", "Silver", "Golden", "Pearl", "Diamond",
    "Sapphire", "Plaza", "Tower", "Heights", "Gardens", "Arcade",
    "Court", "Enclave", "Square", "Centre", "Point", "Hub"
]

# Donor names
DONOR_NAMES = [
    "Taj Hotel", "Hyatt Hyderabad", "Novotel", "ITC Hotels", "Grand Hotel",
    "Radisson Blu", "Marriott", "Four Seasons", "Oakwood Residence", "Best Western",
    "Suntech Restaurant", "Spice Route", "Biryani House", "Curry King", "Royal Feast",
    "Flavors Kitchen", "Taste of India", "Masala Station", "Golden Fork", "Silver Spoon",
    "Paradise Caterers", "Elite Catering", "Star Catering", "Quality Catering", "Royal Catering",
    "Fresh Foods India", "National Foods", "Metro Catering", "Regional Foods", "City Catering",
    "Corporate Cafe", "Office Catering", "Business Kitchen", "Professional Catering", "Smart Foods",
    "Heritage Hotel Resto", "Classic Dining", "Traditional Restaurant", "Authentic Kitchen", "Flavor Palace",
    "Quick Service", "Fast Catering", "Express Foods", "Instant Kitchen", "Speed Service"
]

# Hunger spot names
HUNGER_SPOT_NAMES = [
    "Asha Orphanage", "Hope Foundation", "Children's Haven", "Smile Welfare", "Care Centre",
    "Sunrise NGO", "Helping Hands", "Community Kitchen", "Food Bank", "Relief Centre",
    "Welfare Society", "Child Protection", "Nutrition Hub", "Support Group", "Aid Centre",
    "Shelter Home", "Safe House", "Sanctuary", "Refuge Centre", "Protection Home",
    "Community Centre", "Youth Hub", "Social Welfare", "Public Service", "Charity Work",
    "Feeding Program", "Meal Centre", "Food Distribution", "Nutrition Programme", "Health Kitchen",
    "Day Care", "After School", "After Care", "Evening Programme", "Weekend Centre",
    "Street Children", "Underprivileged Support", "Destitute Care", "Street Aid", "Support Service"
]

# Vehicle prefixes for license plates
VEHICLE_PREFIXES = [
    "TS08", "TS07", "TS06", "TS05", "TS04", "TS03", "TS02", "TS01",
    "AP19", "AP18", "AP17", "AP16"
]

# Contact persons
FIRST_NAMES = [
    "Raj", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Arun", "Divya",
    "Sanjay", "Pooja", "Arjun", "Shreya", "Nikhil", "Deepa", "Rohit", "Sneha",
    "Suresh", "Ananya", "Bhavesh", "Meera", "Hemant", "Ritu", "Kamal", "Sunita"
]

LAST_NAMES = [
    "Sharma", "Singh", "Patel", "Gupta", "Kumar", "Reddy", "Rao", "Nair",
    "Iyer", "Desai", "Verma", "Mishra", "Pandey", "Tripathi", "Saxena", "Kapoor",
    "Walia", "Grover", "Menon", "Bhat", "Hegde", "Kulkarni", "Deshpande"
]

SEED_COUNT = 5  # Number of records to seed for each entity (users, donors, hunger spots, vehicles)

COMMON_PASSWORD = "Password@123"
PINCODE = " - 500000"  # Generic Hyderabad pincode
ADMIN_ROLE_ID = 1  # Role ID for ADMIN
COORDINATOR_ROLE_ID = 2  # Role ID for COORDINATOR
DRIVER_ROLE_ID = 3  # Role ID for DRIVER


def generate_phone_number() -> str:
    """Generate random 10-digit phone number"""
    return f"9{random.randint(100000000, 999999999)}"


def generate_email(first_name: str) -> str:
    """Generate random email"""
    domain = random.choice(["gmail.com", "yahoo.com", "outlook.com"])
    return f"{first_name.lower()}{random.randint(100, 999)}@{domain}"


def generate_address(area: str, name_prefix: str = "") -> str:
    """Generate realistic Hyderabad address"""
    base_pattern = random.choice(ADDRESS_PATTERNS)
    building = random.choice(BUILDING_NAMES)
    
    replacements = {
        "{num}": str(random.randint(1, 500)),
        "{letter}": random.choice(string.ascii_uppercase),
        "{area}": area,
        "{pin}": PINCODE,
        "{name}": f"{name_prefix} {building}" if name_prefix else building
    }
    
    address = base_pattern
    for placeholder, value in replacements.items():
        address = address.replace(placeholder, value)
    
    return address


def generate_gps_coordinates(area: str) -> tuple:
    """
    Get REAL Hyderabad GPS coordinates for the given area.
    Returns (latitude, longitude)
    """
    if area in HYDERABAD_AREAS_WITH_COORDS:
        return HYDERABAD_AREAS_WITH_COORDS[area]
    else:
        # Fallback to city center if area not found
        return (17.3650, 78.4734)


def generate_vehicle_number() -> str:
    """Generate unique Telangana vehicle license plate"""
    prefix = random.choice(VEHICLE_PREFIXES)
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = f"{random.randint(1000, 9999)}"
    return f"{prefix}{letters}{numbers}"


async def seed_inital_admin_coord_driver():
    """Seed initial admin user with DRIVER role and a vehicle for testing"""
    async with AsyncSession(engine) as db:
        first_name = "Admin"
        last_name = "Account"
        name = f"{first_name} {last_name}"
        phone = "9000000001"
        email = "admin_account@nfw.com"
        password_hash = hash_password(COMMON_PASSWORD)
                
        user = User(
            name=name,
            mobile_number=phone,
            email=email,
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        db.add(user)
            
        await db.flush()  # Get IDs before committing
        print(f"   ✓ Created initial admin user: Phone: {phone}, Password: {COMMON_PASSWORD}")
            
        
        user_role = UserRole(
            user_id=user.user_id,
            role_id=ADMIN_ROLE_ID
        )
        db.add(user_role)
        await db.flush()
        print(f"   ✓ Added role for initial admin user")

        first_name = "Coordinator"
        last_name = "Account"
        name = f"{first_name} {last_name}"
        phone = "8000000001"
        email = "coordinator_account@nfw.com"
        password_hash = hash_password(COMMON_PASSWORD)
                
        user = User(
            name=name,
            mobile_number=phone,
            email=email,
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        db.add(user)
            
        await db.flush()  # Get IDs before committing
        print(f"   ✓ Created initial coordinator user: Phone: {phone}, Password: {COMMON_PASSWORD}")
            
        
        user_role = UserRole(
            user_id=user.user_id,
            role_id=COORDINATOR_ROLE_ID
        )
        db.add(user_role)
        await db.flush()
        print(f"   ✓ Added role for initial coordinator user")


        first_name = "Driver"
        last_name = "Account"
        name = f"{first_name} {last_name}"
        phone = "7000000001"
        email = "driver_account@nfw.com"
        password_hash = hash_password(COMMON_PASSWORD)
                
        user = User(
            name=name,
            mobile_number=phone,
            email=email,
            password_hash=password_hash,
            is_active=True,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        db.add(user)
            
        await db.flush()  # Get IDs before committing
        print(f"   ✓ Created initial driver user: Phone: {phone}, Password: {COMMON_PASSWORD}")
            
        
        user_role = UserRole(
            user_id=user.user_id,
            role_id=DRIVER_ROLE_ID
        )
        db.add(user_role)
        await db.flush()
        print(f"   ✓ Added role for initial driver user")
        
        # Commit all changes
        await db.commit()
        
        print("\n" + "="*60)
        print("✅ Added initial admin, coordinator, and driver accounts successfully!")
        print("="*60)
        


async def seed_test_data():
    """Main seed function"""
    print("🌱 Starting test data seeding...\n")
    
    async with AsyncSession(engine) as db:
        try:
            # ============= 1. SEED DRIVERS (ALL USERS ARE DRIVERS) =============
            print(f"👥 Seeding {SEED_COUNT} Drivers...")
            users = []
            for i in range(1, SEED_COUNT + 1):
                first_name = random.choice(FIRST_NAMES)
                last_name = random.choice(LAST_NAMES)
                name = f"{first_name} {last_name}"
                phone = generate_phone_number()
                email = generate_email(first_name)
                password_hash = hash_password(COMMON_PASSWORD)
                
                user = User(
                    name=name,
                    mobile_number=phone,
                    email=email,
                    password_hash=password_hash,
                    is_active=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(user)
                users.append(user)
            
            await db.flush()  # Get IDs before committing
            print(f"   ✓ Created {SEED_COUNT} drivers")
            
            # ============= 2. ASSIGN DRIVER ROLE TO ALL USERS =============
            print("🚗 Assigning DRIVER role to all users...")
            for user in users:
                user_role = UserRole(
                    user_id=user.user_id,
                    role_id=DRIVER_ROLE_ID
                )
                db.add(user_role)
            
            await db.flush()
            print(f"   ✓ All {len(users)} users assigned DRIVER role")
            
            # ============= 3. SEED DONORS =============
            print(f"\n🍽️  Seeding {SEED_COUNT} Donors (Hyderabad)...")
            donors = []
            used_phones = set()

            for i in range(1, SEED_COUNT + 1):
                area = random.choice(HYDERABAD_AREAS)
                donor_name = random.choice(DONOR_NAMES)
                contact_person = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                
                # Ensure unique phone
                phone = generate_phone_number()
                while phone in used_phones:
                    phone = generate_phone_number()
                used_phones.add(phone)
                
                latitude, longitude = generate_gps_coordinates(area)
                address = generate_address(area, donor_name)

                donor = Donor(
                    creator_id=random.choice(users).user_id,
                    donor_name=donor_name,
                    city="Hyderabad",
                    pincode="500000",
                    contact_person=contact_person,
                    mobile_number=phone,
                    address=address,
                    location=address,
                    latitude=latitude,
                    longitude=longitude,
                    is_active=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(donor)
                donors.append(donor)
            
            await db.flush()
            print(f"   ✓ Created {SEED_COUNT} donors across Hyderabad areas")

            # ============= 4. SEED HUNGER SPOTS =============
            print(f"💝 Seeding {SEED_COUNT} Hunger Spots (Hyderabad)...")
            hunger_spots = []
            used_phones_hs = set()

            for i in range(1, SEED_COUNT + 1):
                area = random.choice(HYDERABAD_AREAS)
                spot_name = random.choice(HUNGER_SPOT_NAMES)
                contact_person = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                
                # Ensure unique phone
                phone = generate_phone_number()
                while phone in used_phones_hs:
                    phone = generate_phone_number()
                used_phones_hs.add(phone)
                
                latitude, longitude = generate_gps_coordinates(area)
                address = generate_address(area, spot_name)

                hunger_spot = HungerSpot(
                    creator_id=random.choice(users).user_id,
                    spot_name=spot_name,
                    city="Hyderabad",
                    pincode="500000",
                    contact_person=contact_person,
                    mobile_number=phone,
                    address=address,
                    location=address,
                    latitude=latitude,
                    longitude=longitude,
                    capacity_meals=random.randint(50, 500),
                    is_active=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(hunger_spot)
                hunger_spots.append(hunger_spot)
            
            await db.flush()
            print(f"   ✓ Created {SEED_COUNT} hunger spots across Hyderabad areas")

            # ============= 5. SEED VEHICLES =============
            print(f"🚗 Seeding {SEED_COUNT} Vehicles...")
            vehicles = []
            used_vehicle_numbers = set()

            for i in range(1, SEED_COUNT + 1):
                vehicle_no = generate_vehicle_number()
                while vehicle_no in used_vehicle_numbers:
                    vehicle_no = generate_vehicle_number()
                used_vehicle_numbers.add(vehicle_no)
                
                vehicle_types = ["Bike", "Auto", "Car", "Van", "Tempo", "Truck"]
                capacity = random.choice([1, 2, 3, 4, 6, 9])
                
                vehicle = Vehicle(
                    vehicle_no=vehicle_no,
                    notes=f"{random.choice(vehicle_types)} - Capacity: {capacity} seats",
                    creator_id=random.choice(users).user_id,
                    is_active=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                db.add(vehicle)
                vehicles.append(vehicle)
            
            await db.flush()
            print(f"   ✓ Created {SEED_COUNT} vehicles with unique license plates")
            
            # Commit all changes
            await db.commit()
            
            print("\n" + "="*60)
            print("✅ Test data seeding completed successfully!")
            print("="*60)
            print(f"""
📊 Summary:
   • Drivers: {len(users)} (all with DRIVER role)
   • Donors: {len(donors)} (all in Hyderabad)
   • Hunger Spots: {len(hunger_spots)} (all in Hyderabad)
   • Vehicles: {len(vehicles)} (unique plates)

🔐 Credentials:
   • Password for all users: {COMMON_PASSWORD}
   • Role: All users are DRIVER (role_id: 3)
   • Use any phone number from seeded data to login

📍 All locations within Hyderabad with REAL GPS coordinates:
   • {len(HYDERABAD_AREAS)} different areas
   • Actual latitude/longitude for each area
   • Realistic addresses and contact persons
   • Various donor & hunger spot types

🚗 Ready for testing drivers!
            """)
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_test_data())
