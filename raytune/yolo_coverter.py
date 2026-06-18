from __future__ import annotations

import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image


@dataclass
class CocoIndex:
    images_by_file: dict[str, dict]
    annotations_by_image: dict[int, list[dict]]
    category_to_class: dict[int, str]


RICE_CLASSES = {
    "Healthy",
    "BrownSpot",
    "Hispa",
    "LeafBlast",
}
COFFEE_FOLDER_TO_CLASS = {
    "0": "LeafMiner",
    "1": "PowderyMildew",
    "2": "Rust",
    "3": "AlgalLeafSpot",
}


def clean_path(value: str) -> str:
    return str(value).replace("\\", "/").strip()


def norm_path(value: str) -> str:
    return clean_path(value).lower()


def has_polygon(segmentation) -> bool:
    return isinstance(segmentation, list) and any(isinstance(poly, list) and len(poly) >= 6 for poly in segmentation)


def build_coco_index(coco_data: dict, domain: str) -> CocoIndex:
    if domain == "rice":
        category_to_class = {
            int(cat["id"]): cat["name"] for cat in coco_data.get("categories", []) if cat.get("name") in RICE_CLASSES
        }
    elif domain == "coffee":
        category_to_class = {
            int(cat["id"]): COFFEE_FOLDER_TO_CLASS[str(cat["name"])]
            for cat in coco_data.get("categories", [])
            if str(cat.get("name")) in COFFEE_FOLDER_TO_CLASS
        }
    else:
        raise ValueError(f"Unknown domain: {domain}")

    images_by_file = {norm_path(img["file_name"]): img for img in coco_data.get("images", [])}
    annotations_by_image: dict[int, list[dict]] = defaultdict(list)
    for ann in coco_data.get("annotations", []):
        category_id = int(ann.get("category_id", -1))
        if category_id not in category_to_class:
            continue
        if not has_polygon(ann.get("segmentation")):
            continue
        annotations_by_image[int(ann["image_id"])].append(ann)
    return CocoIndex(images_by_file, dict(annotations_by_image), category_to_class)


def coco_file_from_row(row: pd.Series, target_domain: str) -> str:
    if "relative_path" in row and pd.notna(row["relative_path"]):
        rel = clean_path(row["relative_path"])
        rel_norm = norm_path(rel)
        marker = "rice_leaf_disease/" if target_domain == "rice" else "coffee_leaf_disease/"
        if marker in rel_norm:
            start = rel_norm.index(marker) + len(marker)
            return rel[start:]
        return rel
    return clean_path(row["file_name"])


def raw_image_path(coco_file_name: str, target_domain: str, raw_root: Path) -> Path:
    raw_domain = "rice_leaf_disease" if target_domain == "rice" else "coffee_leaf_disease"
    return raw_root / raw_domain / coco_file_name


def polygon_to_yolo(poly: list[float], width: int, height: int) -> list[float] | None:
    coords = np.asarray(poly, dtype=np.float32).reshape(-1, 2)
    if coords.shape[0] < 3:
        return None
    coords[:, 0] = np.clip(coords[:, 0] / float(width), 0.0, 1.0)
    coords[:, 1] = np.clip(coords[:, 1] / float(height), 0.0, 1.0)
    if np.unique(coords, axis=0).shape[0] < 3:
        return None
    return coords.reshape(-1).tolist()


def reset_dataset_dir(dataset_dir: Path) -> None:
    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)
    for split in ["train", "val", "test"]:
        (dataset_dir / "images" / split).mkdir(parents=True, exist_ok=True)
        (dataset_dir / "labels" / split).mkdir(parents=True, exist_ok=True)


def generate_splits(
    coco_data: dict,
    target_domain: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 3407,
) -> pd.DataFrame:
    coco_index = build_coco_index(coco_data, target_domain)

    valid_images = []
    for img in coco_data.get("images", []):
        img_id = int(img["id"])
        annotations = coco_index.annotations_by_image.get(img_id, [])
        if not annotations:
            continue

        # Pick category of the first annotation
        first_ann = annotations[0]
        cat_id = int(first_ann["category_id"])
        class_name = coco_index.category_to_class[cat_id]

        valid_images.append(
            {
                "sample_id": str(img_id),
                "file_name": img["file_name"],
                "label": class_name,
                "domain": target_domain,
                "relative_path": img["file_name"],
                "class_folder": img["file_name"].split("/")[0] if "/" in img["file_name"] else "",
            }
        )

    df = pd.DataFrame(valid_images)
    if df.empty:
        raise RuntimeError(f"No valid images with annotations found for domain {target_domain}")

    from sklearn.model_selection import train_test_split

    class_counts = df["label"].value_counts()
    min_count = class_counts.min()
    stratify_cols = df["label"] if min_count >= 2 else None

    train_val_df, test_df = train_test_split(df, test_size=test_ratio, random_state=seed, stratify=stratify_cols)

    class_counts_tv = train_val_df["label"].value_counts()
    min_count_tv = class_counts_tv.min()
    stratify_cols_tv = train_val_df["label"] if min_count_tv >= 2 else None

    val_relative_ratio = val_ratio / (train_ratio + val_ratio)

    train_df, val_df = train_test_split(
        train_val_df, test_size=val_relative_ratio, random_state=seed, stratify=stratify_cols_tv
    )

    train_df = train_df.copy()
    train_df["split"] = "train"
    val_df = val_df.copy()
    val_df["split"] = "val"
    test_df = test_df.copy()
    test_df["split"] = "test"

    final_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    return final_df


def convert_to_yolo(
    df: pd.DataFrame,
    target_domain: str,
    raw_root: Path,
    dataset_dir: Path,
    artifacts_dir: Path,
    coco_index: CocoIndex,
    domain_class_to_id: dict[str, int],
) -> pd.DataFrame:
    reset_dataset_dir(dataset_dir)
    rows: list[dict] = []
    skipped: list[tuple[str, str]] = []

    for _, row in df.iterrows():
        coco_file = coco_file_from_row(row, target_domain)
        image_info = coco_index.images_by_file.get(norm_path(coco_file))
        if image_info is None:
            skipped.append((str(row["sample_id"]), "missing_coco_image"))
            continue
        annotations = coco_index.annotations_by_image.get(int(image_info["id"]), [])
        if not annotations:
            skipped.append((str(row["sample_id"]), "missing_polygon_annotation"))
            continue

        src_image = raw_image_path(coco_file, target_domain, raw_root)
        if not src_image.exists():
            raise FileNotFoundError(f"Raw image file not found at: {src_image}")

        split = str(row["split"])
        suffix = src_image.suffix.lower() or ".jpg"
        dst_stem = str(row["sample_id"])
        dst_image = dataset_dir / "images" / split / f"{dst_stem}{suffix}"
        dst_label = dataset_dir / "labels" / split / f"{dst_stem}.txt"
        shutil.copy2(src_image, dst_image)

        width = int(image_info.get("width") or Image.open(src_image).width)
        height = int(image_info.get("height") or Image.open(src_image).height)
        lines: list[str] = []
        for ann in annotations:
            class_name = coco_index.category_to_class[int(ann["category_id"])]
            class_id = domain_class_to_id[class_name]
            for poly in ann.get("segmentation", []):
                yolo_poly = polygon_to_yolo(poly, width, height)
                if yolo_poly is None:
                    continue
                coord_text = " ".join(f"{v:.6f}" for v in yolo_poly)
                lines.append(f"{class_id} {coord_text}")

        if not lines:
            dst_image.unlink(missing_ok=True)
            skipped.append((str(row["sample_id"]), "no_valid_polygon_after_clip"))
            continue

        dst_label.write_text("\n".join(lines) + "\n", encoding="utf-8")
        rows.append(
            {
                **row.to_dict(),
                "image_path_yolo": str(dst_image),
                "label_path": str(dst_label),
                "num_segments": len(lines),
                "coco_file": coco_file,
            }
        )

    converted = pd.DataFrame(rows)
    if converted.empty:
        raise RuntimeError(f"No converted samples for {target_domain}. First skipped examples: {skipped[:10]}")

    skipped_df = pd.DataFrame(skipped, columns=["sample_id", "reason"])
    skipped_df.to_csv(artifacts_dir / f"{target_domain}_conversion_skipped.csv", index=False)
    converted.to_csv(artifacts_dir / f"{target_domain}_converted_manifest.csv", index=False)
    return converted
