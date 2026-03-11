from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from app.core.config import settings
from app.routes import auth_router, health, user_router, role_router, user_role_router, feature_flag_router, vehicle_router, donor_router, hunger_spot_router, opportunity_router, opportunity_item_router, opportunity_event_router, opportunity_allocation_router, opportunity_event_item_driver_router, google_drive_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# -------------------------
# CORS Middleware
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing. Restrict in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# Root helper
# -------------------------
from fastapi.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# -------------------------
# Routers
# -------------------------
app.include_router(health.router, prefix="/api")
app.include_router(auth_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(role_router.router, prefix="/api")
app.include_router(feature_flag_router.router, prefix="/api")
app.include_router(user_role_router.router, prefix="/api")
app.include_router(donor_router.router, prefix="/api")
app.include_router(hunger_spot_router.router, prefix="/api")
app.include_router(opportunity_router.router, prefix="/api")
app.include_router(opportunity_item_router.router, prefix="/api")
app.include_router(opportunity_event_router.router, prefix="/api")
app.include_router(opportunity_allocation_router.router, prefix="/api")
app.include_router(vehicle_router.router, prefix="/api")
app.include_router(google_drive_router.router, prefix="/api")
app.include_router(opportunity_event_item_driver_router.router, prefix="/api")


