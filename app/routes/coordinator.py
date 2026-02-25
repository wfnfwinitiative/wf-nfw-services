from fastapi import APIRouter, Depends
from app.core.dependencies import require_role

router = APIRouter(
    prefix="/coordinator",
    tags=["Coordinator"],
    dependencies=[Depends(require_role(["ADMIN", "COORDINATOR"]))],
)

# ---------------- OPPORTUNITIES ----------------


@router.post("/opportunities")
async def create_opportunity():
    return {"message": "Coordinator create opportunity"}


@router.put("/opportunities/{opportunity_id}")
async def update_opportunity(opportunity_id: int):
    return {"message": f"Coordinator update opportunity {opportunity_id}"}


@router.delete("/opportunities/{opportunity_id}")
async def delete_opportunity(opportunity_id: int):
    return {"message": f"Coordinator delete opportunity {opportunity_id}"}


# ---------------- OPPORTUNITY EVENTS ----------------


@router.post("/opportunity-events")
async def create_event():
    return {"message": "Coordinator create opportunity event"}


@router.put("/opportunity-events/{event_id}")
async def update_event(event_id: int):
    return {"message": f"Coordinator update event {event_id}"}
