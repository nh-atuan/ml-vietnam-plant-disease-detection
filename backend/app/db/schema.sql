-- PostgreSQL schema skeleton

CREATE TABLE IF NOT EXISTS images (
    id UUID PRIMARY KEY,
    object_key TEXT NOT NULL,
    original_filename TEXT,
    content_type TEXT,
    size_bytes BIGINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY,
    image_id UUID REFERENCES images(id),
    predicted_label TEXT NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    top_k JSONB NOT NULL,
    model_version TEXT,
    latency_ms DOUBLE PRECISION,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_predictions_label ON predictions(predicted_label);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
