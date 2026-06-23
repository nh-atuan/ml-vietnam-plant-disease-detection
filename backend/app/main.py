"""
FastAPI Backend — Main application entry point.

Phụ trách: Đàm Tiến Đạt
Phase 5, Task 5.2

Cách chạy:
    uvicorn backend.app.main:app --reload

TODO:
- [ ] Kết nối PostgreSQL (log dự đoán)
- [ ] Kết nối MinIO (lưu ảnh upload)
- [ ] Kết nối Redis (cache kết quả, TTL 1h)
- [ ] Include router predict
- [ ] CORS middleware
- [ ] Health check endpoint
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
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


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

