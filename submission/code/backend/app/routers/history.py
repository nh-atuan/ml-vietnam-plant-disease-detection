"""
Prediction history routes for authenticated users.
"""

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, func, select

from backend.app.config import settings
from backend.app.db import Prediction, crud, get_session
from backend.app.db.orm_models import User
from backend.app.models.schemas import HistoryItem, HistoryResponse
from backend.app.security import get_current_user
from backend.app.services.storage import StorageService

router = APIRouter(prefix="/history", tags=["history"])


def _build_image_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    try:
        storage = StorageService(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            bucket=settings.MINIO_BUCKET,
            secure=settings.MINIO_SECURE,
        )
        return storage.get_url(object_key)
    except Exception:
        return None


@router.get("", response_model=HistoryResponse)
def list_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    skip = (page - 1) * page_size
    rows = crud.get_predictions_by_user(session, current_user.id, skip=skip, limit=page_size)
    total = session.exec(
        select(func.count()).select_from(Prediction).where(Prediction.user_id == current_user.id)
    ).one()
    return HistoryResponse(
        items=[
            HistoryItem(
                id=str(row.id),
                image_id=str(row.image_id),
                predicted_label=row.predicted_label,
                confidence=row.confidence,
                top_k=row.top_k,
                recommendation=row.recommendation,
                image_url=_build_image_url(row.image.object_key if row.image else None),
                created_at=row.created_at,
            )
            for row in rows
        ],
        total=total,
        page=page,
        page_size=page_size,
    )
