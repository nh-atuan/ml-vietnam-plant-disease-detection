"""
CRUD (Create, Read, Update, Delete) operations using SQLModel.
"""
from typing import List, Optional
import uuid
from passlib.context import CryptContext
from sqlmodel import Session, select
from backend.app.db.orm_models import User, Image, Prediction

# Setup CryptContext for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed representation."""
    return pwd_context.verify(plain_password, hashed_password)


# --- User CRUD ---

def create_user(session: Session, username: str, email: str, password: str) -> User:
    """Create a new user with hashed password."""
    hashed_pwd = hash_password(password)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_pwd
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Retrieve a user by their username."""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: uuid.UUID) -> Optional[User]:
    """Retrieve a user by their ID."""
    return session.get(User, user_id)


# --- Image CRUD ---

def create_image_record(
    session: Session,
    object_key: str,
    user_id: Optional[uuid.UUID] = None,
    original_filename: Optional[str] = None,
    content_type: Optional[str] = None,
    size_bytes: Optional[int] = None
) -> Image:
    """Save upload metadata for an image."""
    db_image = Image(
        user_id=user_id,
        object_key=object_key,
        original_filename=original_filename,
        content_type=content_type,
        size_bytes=size_bytes
    )
    session.add(db_image)
    session.commit()
    session.refresh(db_image)
    return db_image


def get_image_by_id(session: Session, image_id: uuid.UUID) -> Optional[Image]:
    """Retrieve an image record by its ID."""
    return session.get(Image, image_id)


# --- Prediction CRUD ---

def create_prediction_record(
    session: Session,
    image_id: uuid.UUID,
    predicted_label: str,
    confidence: float,
    top_k: List[dict],
    user_id: Optional[uuid.UUID] = None,
    recommendation: Optional[dict] = None,
    model_version: Optional[str] = None,
    latency_ms: Optional[float] = None
) -> Prediction:
    """Save prediction details."""
    db_prediction = Prediction(
        image_id=image_id,
        user_id=user_id,
        predicted_label=predicted_label,
        confidence=confidence,
        top_k=top_k,
        recommendation=recommendation,
        model_version=model_version,
        latency_ms=latency_ms
    )
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return db_prediction


def get_predictions_by_user(
    session: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 10
) -> List[Prediction]:
    """Retrieve history of predictions for a given user with pagination."""
    statement = (
        select(Prediction)
        .where(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_prediction_detail(session: Session, prediction_id: uuid.UUID) -> Optional[Prediction]:
    """Retrieve detailed prediction log by ID."""
    return session.get(Prediction, prediction_id)
