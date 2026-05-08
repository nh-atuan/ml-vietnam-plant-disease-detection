"""
Inference Service — ONNX Runtime inference.

Phụ trách: Đàm Tiến Đạt
Phase 5, Task 5.2

TODO:
- [ ] Load ONNX model
- [ ] Preprocess ảnh (resize, normalize theo normalization_stats)
- [ ] Run inference
- [ ] Post-process: softmax → top-k predictions
"""

from typing import List, Tuple
import numpy as np


class InferenceService:
    """ONNX Runtime inference service."""

    def __init__(self, model_path: str, class_names: List[str]):
        # TODO: Load ONNX model với onnxruntime
        raise NotImplementedError

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """Tiền xử lý ảnh từ bytes → tensor."""
        # TODO: Implement (resize, normalize, transpose)
        raise NotImplementedError

    def predict(self, image_bytes: bytes, top_k: int = 5) -> List[Tuple[str, float]]:
        """Dự đoán và trả về top-k (label, confidence)."""
        # TODO: Implement
        raise NotImplementedError
