"""
ONNX Runtime inference service for the FastAPI backend.
"""

import io
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image


class InferenceService:
    """ONNX Runtime inference service."""

    def __init__(self, model_path: str, class_names: list[str], input_size: int = 640):
        model_file = Path(model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"ONNX model not found: {model_path}")
        if not class_names:
            raise ValueError("class_names must not be empty")

        self.session = ort.InferenceSession(str(model_file), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.class_names = class_names
        self.input_size = input_size

    @staticmethod
    def load_class_names(path: str) -> list[str]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, list):
            return [str(item) for item in data]
        if isinstance(data, dict):
            names = data.get("names", data)
            if isinstance(names, dict):
                return [
                    str(names[key])
                    for key in sorted(names, key=lambda value: int(value) if str(value).isdigit() else value)
                ]
            if isinstance(names, list):
                return [str(item) for item in names]
        raise ValueError(f"Unsupported class names format: {path}")

    def preprocess(self, image_bytes: bytes) -> np.ndarray:
        """Convert image bytes to a normalized NCHW float32 tensor."""
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((self.input_size, self.input_size))
        array = np.asarray(image, dtype=np.float32) / 255.0
        array = np.transpose(array, (2, 0, 1))
        return np.expand_dims(array, axis=0).astype(np.float32)

    @staticmethod
    def _softmax(scores: np.ndarray) -> np.ndarray:
        scores = scores.astype(np.float32)
        scores = scores - np.max(scores)
        exp_scores = np.exp(scores)
        return exp_scores / np.sum(exp_scores)

    def _class_scores_from_output(self, output: np.ndarray) -> np.ndarray:
        output = np.asarray(output)
        if output.ndim == 3 and output.shape[0] == 1:
            output = output[0]
            if output.shape[0] < output.shape[1]:
                output = output.T
            class_count = len(self.class_names)
            if output.shape[1] >= 4 + class_count:
                return output[:, 4 : 4 + class_count].max(axis=0)
        if output.ndim == 2:
            if output.shape[0] == 1:
                output = output[0]
            elif output.shape[1] == len(self.class_names):
                return output.max(axis=0)
        if output.ndim == 1 and output.shape[0] >= len(self.class_names):
            return output[: len(self.class_names)]
        raise ValueError(f"Unsupported ONNX output shape: {output.shape}")

    def predict(self, image_bytes: bytes, top_k: int = 5) -> list[tuple[str, float]]:
        """Run inference and return top-k (label, confidence) pairs."""
        tensor = self.preprocess(image_bytes)
        outputs = self.session.run(None, {self.input_name: tensor})
        scores = self._class_scores_from_output(outputs[0])
        probabilities = self._softmax(scores)
        k = min(top_k, len(self.class_names))
        indexes = np.argsort(probabilities)[::-1][:k]
        return [(self.class_names[index], float(probabilities[index])) for index in indexes]
