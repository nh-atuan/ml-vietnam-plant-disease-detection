"""SAM 3 segmentation skeleton."""

from __future__ import annotations

from pathlib import Path


class SAM3Segmenter:
    """Thin placeholder around the future SAM 3 segmentation pipeline."""

    def __init__(self, model_name: str = "facebook/sam3", device: str = "cpu") -> None:
        self.model_name = model_name
        self.device = device

    def segment_image(self, image_path: Path) -> dict:
        """Return segmentation metadata for one image."""
        raise NotImplementedError(f"SAM 3 segmentation is not implemented yet: {image_path}")
