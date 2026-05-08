"""
Robustness Evaluation — Đánh giá độ bền mô hình trước nhiễu thực địa.

Phụ trách: Nguyễn Hồ Anh Tuấn (Sáng tạo S5)
Phase 4, Task 4.7

TODO:
- [ ] Tạo test set nhiễu tổng hợp (blur, brightness, contrast)
- [ ] Đo F1 drop theo mức nhiễu (nhẹ / trung bình / mạnh)
- [ ] So sánh robustness giữa các mô hình
- [ ] Vẽ biểu đồ degradation curve
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, List, Any, Optional


class RobustnessEvaluator:
    """
    Đánh giá robustness bằng cách thêm nhiễu tổng hợp vào test set.

    Loại nhiễu:
    - Gaussian blur (sigma: 1.0, 2.0, 3.0)
    - Brightness shift (±10%, ±20%, ±30%)
    - Contrast change (×0.7, ×0.5, ×0.3)

    Args:
        model: PyTorch model
        test_loader: DataLoader cho tập test sạch
        class_names: List tên lớp
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

    def apply_noise(self, images: torch.Tensor, noise_type: str, level: float) -> torch.Tensor:
        """Thêm nhiễu vào batch ảnh."""
        # TODO: Implement blur, brightness, contrast
        raise NotImplementedError

    def evaluate_with_noise(self, noise_type: str, levels: List[float]) -> Dict[str, Any]:
        """Đánh giá model với một loại nhiễu ở nhiều mức."""
        # TODO: Implement
        raise NotImplementedError

    def full_robustness_report(self) -> Dict[str, Any]:
        """Chạy tất cả loại nhiễu, trả về báo cáo tổng hợp."""
        # TODO: Implement
        raise NotImplementedError

    def plot_degradation_curves(self, save_path: Optional[str] = None):
        """Vẽ biểu đồ F1 drop theo mức nhiễu."""
        # TODO: Implement
        raise NotImplementedError
