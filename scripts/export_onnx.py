"""Export the selected PyTorch checkpoint to ONNX."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export best plant disease model to ONNX.")
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--model-name", type=str, required=True)
    parser.add_argument("--num-classes", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("models/best_model.onnx"))
    parser.add_argument("--opset", type=int, default=17)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raise NotImplementedError(f"ONNX export skeleton is ready for {args.model_name}: {args.output}")


if __name__ == "__main__":
    main()
