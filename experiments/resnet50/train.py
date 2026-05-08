"""
ResNet50 Training Entry Point.

Phụ trách: Đàm Tiến Đạt
Phase 3, Task 3.5

Cách chạy:
    python experiments/resnet50/train.py --config configs/models/resnet50.yaml

TODO:
- [ ] Load config (merge training_defaults + resnet50.yaml)
- [ ] Khởi tạo model ResNet50 từ ModelFactory
- [ ] Khởi tạo DataLoader
- [ ] Khởi tạo BaseTrainer với callbacks
- [ ] Chạy trainer.fit()
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


def parse_args():
    parser = argparse.ArgumentParser(description="Train ResNet50")
    parser.add_argument("--config", type=str, default="configs/models/resnet50.yaml")
    parser.add_argument("--resume", type=str, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    # TODO: Implement training pipeline (xem mobilenetv2/train.py làm mẫu)
    print("ResNet50 training — TODO: implement")


if __name__ == "__main__":
    main()
