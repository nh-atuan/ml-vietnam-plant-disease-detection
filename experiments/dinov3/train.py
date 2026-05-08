"""
DINOv3 Fine-tune Training Entry Point.

Phụ trách: Dương Tuấn Anh (Sáng tạo S2)
Phase 3, Task 3.7

Cách chạy:
    python experiments/dinov3/train.py --config configs/models/dinov3.yaml
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


def parse_args():
    parser = argparse.ArgumentParser(description="Train DINOv3 fine-tune")
    parser.add_argument("--config", type=str, default="configs/models/dinov3.yaml")
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["linear_probing", "full_finetune"],
        default="linear_probing",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    # TODO: Implement DINOv3 training pipeline
    # Lưu ý: DINOv2 model load bằng torch.hub.load('facebookresearch/dinov2', ...)
    print(f"DINOv3 training (strategy={args.strategy}) — TODO: implement")


if __name__ == "__main__":
    main()
