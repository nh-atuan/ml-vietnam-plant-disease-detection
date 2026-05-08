# API Specification

Phụ trách: Tống Thanh Phúc

Phase 5, Task 5.5 output for frontend-backend contract review.

## Health Check

`GET /health`

Response:

```json
{
  "status": "ok"
}
```

## Predict

`POST /api/v1/predict`

Content type: `multipart/form-data`

Form fields:

| Field | Type | Required | Description |
|---|---|---:|---|
| `file` | image file | yes | Leaf image captured from phone or uploaded by user. |

Response shape:

```json
{
  "prediction": "BrownSpot",
  "confidence": 0.92,
  "top_k": [
    {"label": "BrownSpot", "confidence": 0.92},
    {"label": "LeafBlast", "confidence": 0.05}
  ],
  "recommendation": {
    "name_vi": "Đốm nâu",
    "name_en": "Brown Spot",
    "description": "Short disease description",
    "treatments": ["Action item"],
    "severity": "medium"
  },
  "image_id": "uuid"
}
```

TODO:

- Add OpenAPI examples after backend implementation.
- Add error responses for invalid file, unsupported model, and storage failure.
- Add `/api/v1/history` if prediction history is included in the final app.
