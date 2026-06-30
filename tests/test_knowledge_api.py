import os

os.environ["SKIP_DB_INIT"] = "true"

import asyncio
from io import BytesIO

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from backend.app.main import app
from backend.app.routers.knowledge import get_knowledge, list_knowledge
from backend.app.routers.predict import build_recommendation, predict, read_valid_image


def test_list_knowledge_returns_supported_diseases():
    response = asyncio.run(list_knowledge())

    assert response.total == 8
    assert len(response.items) == 8
    assert response.items[0].label
    assert response.items[0].crop
    assert response.items[0].name_vi
    assert response.items[0].name_en
    assert response.items[0].severity


def test_get_knowledge_returns_disease_detail():
    response = asyncio.run(get_knowledge("BrownSpot"))

    assert response.label == "BrownSpot"
    assert response.crop == "rice"
    assert response.treatments
    assert response.prevention
    assert response.sources


def test_get_knowledge_returns_404_for_unknown_label():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(get_knowledge("InvalidLabel"))
    assert exc_info.value.status_code == 404


def test_openapi_contains_knowledge_and_prediction_contracts():
    payload = app.openapi()
    assert "/api/v1/knowledge" in payload["paths"]
    assert "/api/v1/knowledge/{disease_label}" in payload["paths"]
    assert "/api/v1/predict" in payload["paths"]
    assert "DiseaseRecommendation" in payload["components"]["schemas"]


def test_predict_recommendation_builder_matches_knowledge_contract():
    recommendation = build_recommendation("LeafBlast", 0.72)

    assert recommendation["label"] == "LeafBlast"
    assert recommendation["confidence"] == 0.72
    assert recommendation["treatments"]
    assert recommendation["prevention"]


def _upload_file(content: bytes, content_type: str = "image/jpeg") -> UploadFile:
    return UploadFile(
        filename="leaf.jpg",
        file=BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )


def test_predict_upload_validation_accepts_supported_image():
    image_bytes = asyncio.run(read_valid_image(_upload_file(b"image-bytes", "image/png")))

    assert image_bytes == b"image-bytes"


def test_predict_upload_validation_rejects_empty_file():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(read_valid_image(_upload_file(b"")))
    assert exc_info.value.status_code == 400


def test_predict_upload_validation_rejects_unsupported_type():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(read_valid_image(_upload_file(b"not-image", "text/plain")))
    assert exc_info.value.status_code == 415


def test_predict_returns_service_unavailable_until_inference_is_configured():
    with pytest.raises(HTTPException) as exc_info:
        asyncio.run(predict(_upload_file(b"image-bytes")))
    assert exc_info.value.status_code == 503
