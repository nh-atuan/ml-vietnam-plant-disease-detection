"""
Metrics — Hàm tính các metrics chuẩn hóa.

Phụ trách: Nguyễn Hồ Anh Tuấn
Phase 4, Task 4.1

TODO:
- [ ] macro_f1_score
- [ ] weighted_f1_score  
- [ ] per_class_precision_recall_f1
- [ ] domain_split_metrics (rice vs coffee)
- [ ] calibration_metrics (ECE, Brier score)
"""

import torch
import numpy as np
from typing import Dict, Tuple


def macro_f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Tính Macro F1-score."""
    # TODO: Implement (hoặc wrap sklearn)
    raise NotImplementedError


def weighted_f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Tính Weighted F1-score."""
    # TODO: Implement
    raise NotImplementedError


def per_class_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, class_names: list
) -> Dict[str, Dict[str, float]]:
    """Precision/Recall/F1/Support per class."""
    # TODO: Implement
    raise NotImplementedError


def domain_split_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    domains: np.ndarray,
) -> Dict[str, Dict[str, float]]:
    """Tính metrics riêng theo domain (rice / coffee)."""
    # TODO: Implement
    raise NotImplementedError


def calibration_metrics(
    y_true: np.ndarray, y_prob: np.ndarray
) -> Dict[str, float]:
    """ECE và Brier score để đo calibration."""
    # TODO: Implement
    raise NotImplementedError
