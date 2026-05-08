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

from fastapi import FastAPI

app = FastAPI(
    title="Plant Disease Detection API",
    description="Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# TODO: Include routers
# from backend.app.routers import predict
# app.include_router(predict.router, prefix="/api/v1")

# TODO: Setup CORS
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(CORSMiddleware, ...)

# TODO: Startup/shutdown events for DB connections
# @app.on_event("startup")
# async def startup():
#     pass
