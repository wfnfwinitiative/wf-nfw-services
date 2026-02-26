from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
import time

from app.core.config import settings
from app.routes import auth_router, health, user_router, role_router, user_role_router, feature_flag_router, vehicle_router, donor_router, hunger_spot_router, opportunity_router, opportunity_item_router, opportunity_event_router, opportunity_allocation_router

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

# -------------------------
# Logging Middleware
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {process_time:.4f}s")
    return response


# -------------------------
# Global Exception Handler
# -------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )


# -------------------------
# Routers
# -------------------------
app.include_router(health.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(role_router.router)
app.include_router(feature_flag_router.router)
app.include_router(user_role_router.router)
app.include_router(donor_router.router)
app.include_router(hunger_spot_router.router)
app.include_router(opportunity_router.router)
app.include_router(opportunity_event_router.router)
app.include_router(opportunity_allocation_router.router)
app.include_router(opportunity_router.router)


