from fastapi import FastAPI
from .routes import health, users


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Skeleton", version="0.1.0")
    app.include_router(health.router)
    app.include_router(users.router)
    return app


app = create_app()