"""
Training Callbacks — EarlyStopping, ModelCheckpoint, MLflowLogger.

Phụ trách: Nguyễn Hồ Anh Tuấn
Phase 3, Task 3.1

TODO:
- [ ] Implement EarlyStopping theo macro F1 (patience configurable)
- [ ] Implement ModelCheckpoint lưu best model theo metric
- [ ] Implement MLflowLogger tự động log params, metrics, artifacts
"""

from typing import Dict, Any, Optional


class Callback:
    """Base callback interface."""

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]) -> bool:
        """Gọi sau mỗi epoch. Return True để dừng training."""
        return False

    def on_train_end(self, logs: Dict[str, Any]):
        """Gọi khi training kết thúc."""
        pass


class EarlyStopping(Callback):
    """
    Dừng training khi metric không cải thiện sau `patience` epochs.

    Args:
        monitor: Tên metric theo dõi (vd: 'val_macro_f1')
        patience: Số epochs chờ trước khi dừng
        mode: 'max' hoặc 'min'
        min_delta: Ngưỡng cải thiện tối thiểu
    """

    def __init__(
        self,
        monitor: str = "val_macro_f1",
        patience: int = 7,
        mode: str = "max",
        min_delta: float = 0.001,
    ):
        # TODO: Implement
        raise NotImplementedError

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]) -> bool:
        # TODO: Implement early stopping logic
        raise NotImplementedError


class ModelCheckpoint(Callback):
    """
    Lưu model checkpoint khi metric cải thiện.

    Args:
        save_dir: Thư mục lưu checkpoint
        monitor: Tên metric theo dõi
        mode: 'max' hoặc 'min'
    """

    def __init__(
        self,
        save_dir: str,
        monitor: str = "val_macro_f1",
        mode: str = "max",
    ):
        # TODO: Implement
        raise NotImplementedError

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]) -> bool:
        # TODO: Save checkpoint if metric improved
        raise NotImplementedError


class MLflowLogger(Callback):
    """
    Log training metrics và artifacts lên MLflow.

    Args:
        experiment_name: Tên experiment trên MLflow
        run_name: Tên run
        tracking_uri: MLflow tracking server URI
    """

    def __init__(
        self,
        experiment_name: str,
        run_name: Optional[str] = None,
        tracking_uri: str = "mlruns",
    ):
        # TODO: Implement MLflow setup
        raise NotImplementedError

    def on_epoch_end(self, epoch: int, logs: Dict[str, float]) -> bool:
        # TODO: Log metrics to MLflow
        raise NotImplementedError

    def on_train_end(self, logs: Dict[str, Any]):
        # TODO: Log final artifacts (confusion matrix, best checkpoint)
        raise NotImplementedError
