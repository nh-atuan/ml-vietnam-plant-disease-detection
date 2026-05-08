"""
Predict Router — Endpoint /predict cho chẩn đoán bệnh.

Phụ trách: Đàm Tiến Đạt
Phase 5, Task 5.2

TODO:
- [ ] POST /predict: nhận file ảnh → trả nhãn + top-k + confidence
- [ ] Tích hợp InferenceService (ONNX Runtime)
- [ ] Tích hợp KnowledgeBase (gợi ý xử lý)
- [ ] Lưu ảnh vào MinIO, log kết quả vào PostgreSQL
- [ ] Cache kết quả vào Redis (TTL 1h)
"""

from fastapi import APIRouter, UploadFile, File

router = APIRouter(tags=["prediction"])


@router.post("/predict")
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
    # TODO: Implement
    raise NotImplementedError("predict endpoint")
