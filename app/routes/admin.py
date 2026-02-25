from fastapi import APIRouter, Depends
from app.core.dependencies import require_role
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.models import AdminCreateUser
from app.services.user_service import create_user_with_role

router = APIRouter(
    prefix="/admin", tags=["Admin"], dependencies=[Depends(require_role(["ADMIN"]))]
)

# ---------------- USERS ----------------


@router.post("/users")
async def create_user(data: AdminCreateUser, db: AsyncSession = Depends(get_db)):
    await create_user_with_role(
        db,
        name=data.name,
        mobile=data.mobile_number,
        password=data.password,
        role_name=data.role,
    )
    return {"message": "User created successfully"}


@router.put("/users/{user_id}")
async def update_user(user_id: int):
    return {"message": f"Admin update user {user_id}"}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    return {"message": f"Admin delete user {user_id}"}


# ---------------- VEHICLES ----------------


@router.post("/vehicles")
async def create_vehicle():
    return {"message": "Admin create vehicle"}


@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    return {"message": f"Admin delete vehicle {vehicle_id}"}


# ---------------- ROLES ----------------


@router.post("/roles")
async def create_role():
    return {"message": "Admin create role"}


# ---------------- HUNGER SPOTS ----------------


@router.post("/hunger-spots")
async def create_hunger_spot():
    return {"message": "Admin create hunger spot"}


# ---------------- DONORS ----------------


@router.post("/donors")
async def create_donor():
    return {"message": "Admin create donor"}


# ---------------- REPORTS ----------------


@router.get("/reports/opportunities")
async def download_opportunity_report():
    return {"message": "Admin download opportunities report"}
