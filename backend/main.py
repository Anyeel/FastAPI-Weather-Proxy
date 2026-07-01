from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.database.session import engine
from backend.models.weather import Base
from backend.routers import weather, forecast


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Weather Proxy MVP",
    version="1.1.0",
    lifespan=lifespan
)

# Apply middleware using config
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # <--- Usamos settings aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather.router)
app.include_router(forecast.router)


@app.get("/", tags=["API Check"])
async def root():
    """Root endpoint to check if the API is running.

    Returns:
        dict: A welcome message and status.
    """
    return {
        "status": "online",
        "message": "Welcome to the Weather Proxy API! Visit /docs for documentation."
    }
