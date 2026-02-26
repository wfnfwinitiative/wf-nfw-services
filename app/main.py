from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from app.core.config import settings
from app.routes import auth, admin, coordinator, driver, health, feature_flag

app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

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
# Routers
# -------------------------
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(coordinator.router)
app.include_router(driver.router)
app.include_router(feature_flag.router)
