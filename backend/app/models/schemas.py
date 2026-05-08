"""
Pydantic Schemas — Request/Response models.

Phụ trách: Đàm Tiến Đạt
Phase 5, Task 5.2

TODO:
- [ ] PredictionResponse schema
- [ ] TopKPrediction schema
- [ ] DiseaseRecommendation schema
- [ ] PredictionLog schema (for PostgreSQL)
"""

from pydantic import BaseModel, Field


class TopKPrediction(BaseModel):
    label: str
    confidence: float


class DiseaseRecommendation(BaseModel):
    name_vi: str
    name_en: str
    description: str | None = None
    treatments: list[str] = Field(default_factory=list)
    severity: str | None = None


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    top_k: list[TopKPrediction]
    recommendation: DiseaseRecommendation | None = None
    image_id: str | None = None


# TODO: Thêm schemas cho PostgreSQL logging, MinIO metadata, etc.
