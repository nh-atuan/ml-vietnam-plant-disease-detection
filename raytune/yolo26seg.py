import time
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from ultralytics import YOLO


def extract_ultralytics_metrics(metrics) -> dict:
    def value(path: str):
        current = metrics
        for part in path.split("."):
            current = getattr(current, part, None)
            if current is None:
                return None
        try:
            return float(current)
        except TypeError:
            return current

    return {
        "mAP50_mask": value("seg.map50"),
        "mAP50_95_mask": value("seg.map"),
        "mAP75_mask": value("seg.map75"),
        "fitness": getattr(metrics, "fitness", None),
    }


def run_train(
    config: dict,
    common_args: dict,
    data_yaml: Path,
    device: str,
) -> dict:
    model = YOLO(config["model"])
    args = {**common_args, **{k: v for k, v in config.items() if k not in {"model"}}}
    args["data"] = str(data_yaml)
    args["device"] = device

    print(f"Training {config['name']} with {config['model']}")
    train_result = model.train(**args)
    best_ckpt = Path(train_result.save_dir) / "weights" / "best.pt"

    row = {
        "run": config["name"],
        "model": config["model"],
        "epochs": config["epochs"],
        "imgsz": common_args["imgsz"],
        "best_ckpt": str(best_ckpt),
        "size_mb": best_ckpt.stat().st_size / (1024 * 1024) if best_ckpt.exists() else None,
    }
    return row


def read_yolo_label(label_path: Path) -> list[tuple[int, np.ndarray]]:
    segments: list[tuple[int, np.ndarray]] = []
    if not label_path.exists():
        return segments
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.strip().split()
        if not parts:
            continue
        class_id = int(parts[0])
        coords = np.asarray([float(v) for v in parts[1:]], dtype=np.float32).reshape(-1, 2)
        segments.append((class_id, coords))
    return segments


def rasterize_label_file(
    label_path: Path,
    width: int,
    height: int,
    domain_classes: list[str],
) -> np.ndarray:
    masks = np.zeros((len(domain_classes), height, width), dtype=bool)
    for class_id, coords in read_yolo_label(label_path):
        if not 0 <= class_id < len(domain_classes):
            continue
        pixel_points = [(float(x) * width, float(y) * height) for x, y in coords]
        mask_img = Image.new("L", (width, height), 0)
        ImageDraw.Draw(mask_img).polygon(pixel_points, outline=1, fill=1)
        masks[class_id] |= np.asarray(mask_img, dtype=bool)
    return masks


def rasterize_predictions(
    result,
    width: int,
    height: int,
    domain_classes: list[str],
) -> np.ndarray:
    masks = np.zeros((len(domain_classes), height, width), dtype=bool)
    if result.masks is None or result.boxes is None or len(result.boxes) == 0:
        return masks
    pred_masks = result.masks.data.detach().cpu().numpy()
    pred_classes = result.boxes.cls.detach().cpu().numpy().astype(int)
    for class_id, mask in zip(pred_classes, pred_masks):
        if not 0 <= int(class_id) < len(domain_classes):
            continue
        mask_bool = mask > 0.5
        if mask_bool.shape != (height, width):
            mask_img = Image.fromarray(mask_bool.astype(np.uint8) * 255).resize(
                (width, height), Image.Resampling.NEAREST
            )
            mask_bool = np.asarray(mask_img, dtype=np.uint8) > 0
        masks[int(class_id)] |= mask_bool
    return masks


def mean_iou_dice(
    gt: np.ndarray,
    pred: np.ndarray,
    domain_classes: list[str],
) -> tuple[float, float, dict, list[str], list[str]]:
    ious = []
    dices = []
    per_class = {}
    gt_classes = []
    pred_classes = []
    for class_id, class_name in enumerate(domain_classes):
        gt_mask = gt[class_id]
        pred_mask = pred[class_id]
        is_gt = gt_mask.any()
        is_pred = pred_mask.any()
        if is_gt:
            gt_classes.append(class_name)
        if is_pred:
            pred_classes.append(class_name)
        if not is_gt and not is_pred:
            continue
        intersection = np.logical_and(gt_mask, pred_mask).sum()
        union = np.logical_or(gt_mask, pred_mask).sum()
        denom = gt_mask.sum() + pred_mask.sum()
        iou = float(intersection / union) if union else 1.0
        dice = float(2 * intersection / denom) if denom else 1.0
        ious.append(iou)
        dices.append(dice)
        per_class[class_name] = {"iou": iou, "dice": dice}
    return (
        float(np.mean(ious)) if ious else 0.0,
        float(np.mean(dices)) if dices else 0.0,
        per_class,
        gt_classes,
        pred_classes,
    )


def evaluate_test_set(
    ckpt: Path,
    df: pd.DataFrame,
    domain_classes: list[str],
    data_yaml: Path,
    imgsz: int = 640,
    device: str = "cpu",
) -> tuple[dict, pd.DataFrame]:
    model = YOLO(str(ckpt))

    # Run standard validation on test split using YOLO to get mAP@50 and mAP@50:95
    val_metrics = model.val(data=str(data_yaml), split="test", imgsz=imgsz, device=device, plots=True, verbose=False)
    yolo_metrics = extract_ultralytics_metrics(val_metrics)

    test_df = df[df["split"] == "test"].copy()
    rows = []

    for _, row in test_df.iterrows():
        image_path = Path(row["image_path_yolo"])
        image = Image.open(image_path).convert("RGB")
        width, height = image.size
        gt = rasterize_label_file(Path(row["label_path"]), width, height, domain_classes)
        result = model.predict(str(image_path), imgsz=imgsz, device=device, verbose=False)[0]
        pred = rasterize_predictions(result, width, height, domain_classes)
        miou, dice, per_class, gt_classes, pred_classes = mean_iou_dice(gt, pred, domain_classes)

        row_dict = {
            "sample_id": row["sample_id"],
            "label": row["label"],
            "mIoU": miou,
            "Dice": dice,
            "gt_classes": ",".join(gt_classes),
            "pred_classes": ",".join(pred_classes),
        }
        # Add per-class IoU and Dice
        for class_name in domain_classes:
            if class_name in per_class:
                row_dict[f"{class_name}_IoU"] = per_class[class_name]["iou"]
                row_dict[f"{class_name}_Dice"] = per_class[class_name]["dice"]
                row_dict[f"{class_name}_present"] = True
            else:
                row_dict[f"{class_name}_IoU"] = None
                row_dict[f"{class_name}_Dice"] = None
                row_dict[f"{class_name}_present"] = False

        rows.append(row_dict)

    score_df = pd.DataFrame(rows)

    # Calculate overall dataset statistics
    summary = {
        "mIoU": float(score_df["mIoU"].mean()) if not score_df.empty else 0.0,
        "Dice": float(score_df["Dice"].mean()) if not score_df.empty else 0.0,
        "mAP50_mask": yolo_metrics["mAP50_mask"],
        "mAP50_95_mask": yolo_metrics["mAP50_95_mask"],
        "n_test_images": int(len(score_df)),
    }

    for class_name in domain_classes:
        # Calculate mean over images where the class was present in either gt or prediction
        subset = score_df[score_df[f"{class_name}_present"]]
        summary[f"{class_name}_IoU"] = float(subset[f"{class_name}_IoU"].mean()) if not subset.empty else 1.0
        summary[f"{class_name}_Dice"] = float(subset[f"{class_name}_Dice"].mean()) if not subset.empty else 1.0

    return summary, score_df


def benchmark_cpu_latency(
    ckpt: Path,
    df: pd.DataFrame,
    imgsz: int = 640,
    n_images: int = 50,
) -> float:
    model = YOLO(str(ckpt))
    test_paths = [Path(p) for p in df[df["split"] == "test"]["image_path_yolo"].head(n_images)]
    if not test_paths:
        return float("nan")

    # Warmup on CPU
    for image_path in test_paths[:3]:
        model.predict(str(image_path), imgsz=imgsz, device="cpu", verbose=False)

    start = time.perf_counter()
    for image_path in test_paths:
        model.predict(str(image_path), imgsz=imgsz, device="cpu", verbose=False)
    elapsed = time.perf_counter() - start

    return elapsed * 1000.0 / len(test_paths)


def overlay_segments(
    image_path: Path,
    label_path: Path,
    alpha: int = 95,
    palette=[
        "#1B9E77",
        "#D95F02",
        "#7570B3",
        "#E7298A",
        "#66A61E",
        "#E6AB02",
        "#A6761D",
        "#666666",
    ],
) -> Image.Image:
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for class_id, coords in read_yolo_label(label_path):
        points = [(float(x) * width, float(y) * height) for x, y in coords]
        rgb = tuple(int(palette[class_id].lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        draw.polygon(points, outline=rgb + (255,), fill=rgb + (alpha,))
    return Image.alpha_composite(image, overlay).convert("RGB")
