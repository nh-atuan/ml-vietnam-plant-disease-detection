"""
FastAPI Backend — Main application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import settings
from backend.app.db import init_db
from backend.app.routers import knowledge, predict


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    if settings.SKIP_DB_INIT:
        yield
        return

    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    yield


app = FastAPI(
    title="Plant Disease Detection API",
    description="Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knowledge.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
