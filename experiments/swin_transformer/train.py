"""
Swin Transformer Training Entry Point.

Phụ trách: Tống Thanh Phúc
Phase 3, Task 3.6

Cách chạy:
    python experiments/swin_transformer/train.py --config configs/models/swin_transformer.yaml
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))


def parse_args():
    parser = argparse.ArgumentParser(description="Train Swin Transformer")
    parser.add_argument("--config", type=str, default="configs/models/swin_transformer.yaml")
    parser.add_argument("--resume", type=str, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    # TODO: Implement training pipeline
    print("Swin Transformer training — TODO: implement")


if __name__ == "__main__":
    main()
