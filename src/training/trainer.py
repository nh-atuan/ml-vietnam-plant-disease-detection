"""
BaseTrainer — Training loop tổng quát cho tất cả mô hình.

Phụ trách: Nguyễn Hồ Anh Tuấn
Phase 3, Task 3.1

TODO:
- [ ] Implement training loop với mixed precision (AMP)
- [ ] Tích hợp callbacks (EarlyStopping, ModelCheckpoint, MLflowLogger)
- [ ] Support resume from checkpoint
- [ ] Log metrics theo epoch lên MLflow
- [ ] Validation loop với macro F1 tracking
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Dict, Any, Optional, List


class BaseTrainer:
    """
    Training loop chuẩn hóa cho toàn bộ mô hình trong project.

    Args:
        model: PyTorch model đã khởi tạo
        train_loader: DataLoader cho tập train
        val_loader: DataLoader cho tập validation
        optimizer: Optimizer (AdamW recommended)
        scheduler: LR scheduler (CosineAnnealingLR / ReduceLROnPlateau)
        criterion: Loss function
        config: Dict chứa training hyperparameters
        callbacks: List các callback objects
        device: 'cuda' hoặc 'cpu'
    """

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        optimizer: torch.optim.Optimizer,
        scheduler: Optional[Any] = None,
        criterion: Optional[nn.Module] = None,
        config: Optional[Dict[str, Any]] = None,
        callbacks: Optional[List] = None,
        device: str = "cpu",
    ):
        # TODO: Implement initialization
        raise NotImplementedError("BaseTrainer.__init__")

    def train_one_epoch(self, epoch: int) -> Dict[str, float]:
        """Train một epoch, trả về dict metrics (loss, accuracy, ...)."""
        # TODO: Implement với AMP (torch.cuda.amp)
        raise NotImplementedError("BaseTrainer.train_one_epoch")

    def validate(self) -> Dict[str, float]:
        """Validate trên val_loader, trả về dict metrics (loss, macro_f1, ...)."""
        # TODO: Implement validation loop
        raise NotImplementedError("BaseTrainer.validate")

    def fit(self, num_epochs: int) -> Dict[str, Any]:
        """
        Main training loop.

        Luồng:
        1. Cho mỗi epoch: train_one_epoch → validate
        2. Gọi callbacks sau mỗi epoch (early stopping, checkpoint, mlflow log)
        3. Apply LR scheduler
        4. Kiểm tra early stopping condition
        5. Return training history
        """
        # TODO: Implement main loop
        raise NotImplementedError("BaseTrainer.fit")

    def save_checkpoint(self, path: str, epoch: int, metrics: Dict[str, float]):
        """Lưu checkpoint (model state, optimizer state, epoch, metrics)."""
        # TODO: Implement checkpoint saving
        raise NotImplementedError("BaseTrainer.save_checkpoint")

    def load_checkpoint(self, path: str) -> int:
        """Load checkpoint và trả về epoch đã train."""
        # TODO: Implement checkpoint loading
        raise NotImplementedError("BaseTrainer.load_checkpoint")
