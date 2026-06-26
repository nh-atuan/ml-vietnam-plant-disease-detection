"""
Configuration settings for the backend application using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "development"
    MODEL_PATH: str = "/models/best_model.onnx"
    CLASS_NAMES_PATH: str = "/models/class_names.json"
    MODEL_INPUT_SIZE: int = 640
    MODEL_VERSION: str = "yolo26-seg-onnx"

    # Authentication
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    JWT_ALGORITHM: str = "HS256"

    # PostgreSQL configuration
    DATABASE_URL: str | None = None
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "plant_disease"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "changeme"

    # Redis configuration
    REDIS_URL: str = "redis://redis:6379/0"

    # MinIO configuration
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "plant-disease-images"
    MINIO_SECURE: bool = False

    # MLflow tracking
    MLFLOW_TRACKING_URI: str = "http://mlflow:5000"

    @property
    def database_url(self) -> str:
        """Returns the PostgreSQL connection string."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
