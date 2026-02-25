from fastapi import APIRouter, Depends
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/driver", tags=["Driver"], dependencies=[Depends(require_role(["DRIVER"]))]
)

# ---------------- OPPORTUNITIES ----------------


@router.post("/opportunities")
async def create_opportunity():
    return {"message": "Driver create opportunity"}


# ---------------- OPPORTUNITY EVENTS ----------------


@router.post("/opportunity-events")
async def create_event():
    return {"message": "Driver create opportunity event"}


@router.put("/opportunity-events/{event_id}")
async def update_event(event_id: int):
    return {"message": f"Driver update opportunity event {event_id}"}
