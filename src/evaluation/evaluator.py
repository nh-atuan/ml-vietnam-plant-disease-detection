"""
Evaluator — Đánh giá chuẩn hóa cho tất cả mô hình.

Phụ trách: Nguyễn Hồ Anh Tuấn
Phase 4, Task 4.1

TODO:
- [ ] Confusion matrix (đếm tuyệt đối + chuẩn hóa theo hàng)
- [ ] Macro F1, Weighted F1, Accuracy — tổng + theo domain (rice/coffee)
- [ ] Per-class Precision/Recall/F1 với support
- [ ] ROC curve one-vs-rest
- [ ] Inference time benchmark (ms/ảnh, throughput)
- [ ] Export kết quả sang dict/JSON chuẩn hóa
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional


class Evaluator:
    """
    Evaluation suite chuẩn hóa.

    Args:
        model: PyTorch model đã load checkpoint
        test_loader: DataLoader cho tập test
        class_names: List tên các lớp
        device: 'cuda' hoặc 'cpu'
    """

    def __init__(
        self,
        model: nn.Module,
        test_loader: DataLoader,
        class_names: list,
        device: str = "cpu",
    ):
        # TODO: Implement
        raise NotImplementedError

    def evaluate(self) -> Dict[str, Any]:
        """
        Chạy full evaluation, trả về dict chứa tất cả metrics.

        Returns:
            {
                'macro_f1': float,
                'weighted_f1': float,
                'accuracy': float,
                'per_class': {...},
                'confusion_matrix': np.ndarray,
                'inference_time_ms': float,
                'model_size_mb': float,
            }
        """
        # TODO: Implement
        raise NotImplementedError

    def confusion_matrix(self) -> Any:
        """Tính confusion matrix (raw counts + normalized)."""
        # TODO: Implement
        raise NotImplementedError

    def per_class_metrics(self) -> Dict[str, Dict[str, float]]:
        """Precision/Recall/F1 per class."""
        # TODO: Implement
        raise NotImplementedError

    def benchmark_inference(self, num_samples: int = 100) -> Dict[str, float]:
        """Benchmark inference time (ms/ảnh) và throughput (ảnh/s)."""
        # TODO: Implement
        raise NotImplementedError

    def plot_confusion_matrix(self, save_path: Optional[str] = None):
        """Vẽ confusion matrix heatmap."""
        # TODO: Implement
        raise NotImplementedError

    def plot_roc_curves(self, save_path: Optional[str] = None):
        """Vẽ ROC curves one-vs-rest."""
        # TODO: Implement
        raise NotImplementedError

    def export_results(self, save_path: str):
        """Export toàn bộ kết quả ra JSON."""
        # TODO: Implement
        raise NotImplementedError
