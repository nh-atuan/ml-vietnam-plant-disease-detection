"""
Pydantic Schemas — Request/Response models.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# --- Prediction Schemas ---

class TopKPrediction(BaseModel):
    label: str
    confidence: float


class DiseaseRecommendation(BaseModel):
    name_vi: str
    name_en: str
    description: Optional[str] = None
    treatments: List[str] = Field(default_factory=list)
    severity: Optional[str] = None


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    top_k: List[TopKPrediction]
    recommendation: Optional[DiseaseRecommendation] = None
    image_id: Optional[str] = None
    image_url: Optional[str] = None


# --- User & Auth Schemas ---

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, examples=["farmer_john"])
    email: str = Field(..., examples=["john@example.com"])
    password: str = Field(..., min_length=6, examples=["secretpass"])


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str = Field(..., examples=["farmer_john"])
    password: str = Field(..., examples=["secretpass"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- History Schemas ---

class HistoryItem(BaseModel):
    id: str
    image_id: str
    predicted_label: str
    confidence: float
    top_k: List[TopKPrediction]
    recommendation: Optional[DiseaseRecommendation] = None
    image_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    items: List[HistoryItem]
    total: int
    page: int
    page_size: int
