"""General-purpose utilities for the plant disease detection project."""

import json
import os
import random
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd


def set_seed(seed: int = 42) -> None:
    """Set random seeds for common libraries and environment.

    Args:
        seed: integer seed to use.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    # For sklearn: pass random_state=seed explicitly.
    # For PyTorch/TF: set their RNGs in the calling script.


def load_coco(path: Path) -> dict:
    """Load a COCO-format annotation JSON file.

    Args:
        path: path to the .json file.

    Returns:
        Parsed COCO dict with keys: info, images, annotations, categories.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_image_df(coco: dict, label_fn: Callable[[str], str]) -> pd.DataFrame:
    """Build a per-image DataFrame from a COCO dict.

    Args:
        coco:     parsed COCO annotation dict.
        label_fn: function that maps file_name → class label string.

    Returns:
        DataFrame with columns: image_id, file_name, width, height,
        label, aspect_ratio.
    """
    rows = []
    for img in coco["images"]:
        rows.append({
            "image_id":     img["id"],
            "file_name":    img["file_name"],
            "width":        img["width"],
            "height":       img["height"],
            "label":        label_fn(img["file_name"]),
            "aspect_ratio": img["width"] / img["height"],
        })
    return pd.DataFrame(rows)


def build_ann_df(coco: dict, cat_map: dict) -> pd.DataFrame:
    """Build a per-annotation DataFrame from a COCO dict.

    Args:
        coco:    parsed COCO annotation dict.
        cat_map: {category_id: display_name} mapping.

    Returns:
        DataFrame with columns: ann_id, image_id, category_id, class_name,
        area, bbox_w, bbox_h, bbox_area.
    """
    rows = []
    for ann in coco["annotations"]:
        bbox = ann.get("bbox", [0, 0, 0, 0])
        rows.append({
            "ann_id":      ann["id"],
            "image_id":    ann["image_id"],
            "category_id": ann["category_id"],
            "class_name":  cat_map.get(ann["category_id"], "unknown"),
            "area":        ann.get("area", 0),
            "bbox_w":      bbox[2],
            "bbox_h":      bbox[3],
        })
    df = pd.DataFrame(rows)
    df["bbox_area"] = df["bbox_w"] * df["bbox_h"]
    return df