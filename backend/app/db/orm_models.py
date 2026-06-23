"""
ORM models for SQLModel database.
"""
from datetime import datetime
from typing import Dict, List, Optional
import uuid
from sqlmodel import Field, Relationship, SQLModel, Column, JSON


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    username: str = Field(unique=True, index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    images: List["Image"] = Relationship(back_populates="user")
    predictions: List["Prediction"] = Relationship(back_populates="user")


class Image(SQLModel, table=True):
    __tablename__: str = "images"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", nullable=True)
    object_key: str = Field(nullable=False)
    original_filename: Optional[str] = Field(default=None, nullable=True)
    content_type: Optional[str] = Field(default=None, nullable=True)
    size_bytes: Optional[int] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    user: Optional[User] = Relationship(back_populates="images")
    predictions: List["Prediction"] = Relationship(back_populates="image")


class Prediction(SQLModel, table=True):
    __tablename__: str = "predictions"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    image_id: uuid.UUID = Field(foreign_key="images.id", nullable=False)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id", nullable=True)
    predicted_label: str = Field(nullable=False, index=True)
    confidence: float = Field(nullable=False)
    
    # Store JSON data in DB
    top_k: List[Dict] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    recommendation: Optional[Dict] = Field(default=None, sa_column=Column(JSON, nullable=True))
    
    model_version: Optional[str] = Field(default=None, nullable=True)
    latency_ms: Optional[float] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)

    # Relationships
    image: Image = Relationship(back_populates="predictions")
    user: Optional[User] = Relationship(back_populates="predictions")
