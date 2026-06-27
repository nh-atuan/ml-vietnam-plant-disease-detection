"""
Predict Router — Endpoint /predict cho chẩn đoán bệnh.
"""

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.knowledge import KnowledgeBase
from backend.app.models.schemas import PredictionResponse

router = APIRouter(tags=["prediction"])
knowledge_base = KnowledgeBase()
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_BYTES = 10 * 1024 * 1024


def build_recommendation(disease_label: str, confidence: float) -> dict:
    """Build the recommendation payload that /predict should attach after inference."""
    return knowledge_base.format_recommendation(disease_label, confidence)


async def read_valid_image(file: UploadFile) -> bytes:
    """Read and validate an uploaded image before inference/storage side effects."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Unsupported image type. Upload a JPEG, PNG, or WEBP image.",
        )

    image_bytes = file.file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")
    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Uploaded image is too large. Maximum size is 10 MB.")
    return image_bytes


@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Nhận ảnh lá cây, trả về kết quả chẩn đoán.

    Response:
    {
        "prediction": "BrownSpot",
        "confidence": 0.92,
        "top_k": [
            {"label": "BrownSpot", "confidence": 0.92},
            {"label": "LeafBlast", "confidence": 0.05},
            ...
        ],
        "recommendation": {
            "name_vi": "Đốm nâu",
            "treatments": [...],
            ...
        }
    }
    """
    await read_valid_image(file)
    raise HTTPException(
        status_code=503,
        detail=(
            "Prediction inference is not configured yet. Export the ONNX model, wire InferenceService, then attach "
            "build_recommendation(label, confidence) to the response."
        ),
    )
