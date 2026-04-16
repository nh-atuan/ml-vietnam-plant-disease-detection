import argparse
import glob
import json
import os
import shutil

import cv2
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
from transformers import Sam3Model, Sam3Processor, Sam3TrackerModel, Sam3TrackerProcessor


def init_model(device: str, click_seg: bool = False):
    print(f"Loading SAM3{' Tracker' if click_seg else ''} models...")

    if click_seg:
        # Promptable Visual Segmentation (PVS) for point clicks
        model = Sam3TrackerModel.from_pretrained("facebook/sam3").to(device)
        processor = Sam3TrackerProcessor.from_pretrained("facebook/sam3")
    else:
        # Promptable Concept Segmentation (PCS) for text/boxes
        model = Sam3Model.from_pretrained("facebook/sam3").to(device)
        processor = Sam3Processor.from_pretrained("facebook/sam3")

    print("Models loaded successfully.")
    return model, processor


def batch_inference(
    model,
    processor,
    device: str,
    images: list[np.ndarray | Image.Image],
    prompts: list[str | None],
    bboxes: list[list[list[float]] | None],
    input_boxes_labels: list[list[int] | None],
    input_points: list[list[list[list[float]]]] | None = None,
    input_points_labels: list[list[list[int]]] | None = None,
    click_seg: bool = False,
    threshold: float = 0.5,
    mask_threshold: float = 0.5,
):
    """Promptable segmentation logic handling both PCS (texts/boxes) and PVS (points)."""
    if click_seg:
        kwargs = {
            "images": images,
            "input_points": input_points,
            "input_labels": input_points_labels,
            "return_tensors": "pt",
        }
        inputs = processor(**kwargs).to(device)

        with torch.no_grad():
            outputs = model(**inputs, multimask_output=False)

        masks = processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"], binarize=True)[0]

        if masks.dim() == 4 and masks.shape[1] == 1:
            masks = masks.squeeze(1)

        print(f"[DEBUG] There are {len(masks)} masks before applying threshold")

        masks = masks > mask_threshold

        print(f"[DEBUG] There are {len(masks)} masks after applying threshold")

        # ========================================================
        # NEW CODE: Save raw mask overlays for debugging
        # ========================================================
        import time

        try:
            # Since click_seg enforces batch_size=1, we grab the first image
            img = images[0]

            # Ensure it is converted to a BGR numpy array for OpenCV
            if hasattr(img, "convert"):  # Check if it's a PIL Image
                img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            else:
                img_cv2 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            overlay_cv2 = img_cv2.copy()
            np_masks = masks.cpu().numpy() if torch.is_tensor(masks) else masks

            for mask_2d in np_masks:
                # Squeeze out extra dimensions if any exist to ensure a strict 2D shape (H, W)
                if mask_2d.ndim > 2:
                    mask_2d = mask_2d.squeeze()

                color = np.random.randint(0, 255, (3,)).tolist()
                colored_mask = np.zeros_like(img_cv2)
                colored_mask[mask_2d > 0] = color

                # Apply 50% opacity to the mask overlay
                cv2.addWeighted(overlay_cv2, 1.0, colored_mask, 0.5, 0, dst=overlay_cv2)

            # Create a dedicated directory and save with a timestamp
            os.makedirs("debug_raw_masks", exist_ok=True)
            save_path = f"debug_raw_masks/raw_mask_{int(time.time() * 1000)}.jpg"
            cv2.imwrite(save_path, overlay_cv2)
            print(f"[DEBUG] Saved raw inference mask overlay to {save_path}")

        except Exception as e:
            print(f"[DEBUG] Failed to save raw mask overlay: {e}")
        # ========================================================

        return [{"masks": masks}]

    else:
        kwargs = {"images": images, "text": prompts, "return_tensors": "pt"}
        has_boxes = bboxes is not None and any(b is not None for b in bboxes)
        if has_boxes:
            kwargs["input_boxes"] = bboxes
            if input_boxes_labels is not None:
                kwargs["input_boxes_labels"] = input_boxes_labels

        inputs = processor(**kwargs).to(device)

        with torch.no_grad():
            outputs = model(**inputs)

        results = processor.post_process_instance_segmentation(
            outputs,
            threshold=threshold,
            mask_threshold=mask_threshold,
            target_sizes=inputs.get("original_sizes").tolist(),
        )
        return results


def mask_to_polygons(mask: np.ndarray) -> list[list[float]]:
    """Convert a binary mask array to COCO-compatible polygon format."""
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    polygons = []
    for contour in contours:
        contour = contour.flatten().tolist()
        if len(contour) >= 6:
            polygons.append(contour)
    return polygons


def process_dataset(dataset_dir: str, batch_size: int, device: str, click_seg: bool = False):
    model, processor = init_model(device, click_seg)

    search_pattern = os.path.join(dataset_dir, "**", "annotations.coco.json")
    json_files = glob.glob(search_pattern, recursive=True)

    if not json_files:
        print(f"No annotations.coco.json found in {dataset_dir}")
        return

    for json_path in json_files:
        print(f"\nProcessing {json_path}...")

        backup_path = json_path + ".bak"
        if not os.path.exists(backup_path):
            shutil.copy2(json_path, backup_path)
            print(f"Created backup at {backup_path}")

        with open(json_path, encoding="utf-8") as f:
            coco_data = json.load(f)

        images_dict = {img["id"]: img for img in coco_data.get("images", [])}
        original_annotations = coco_data.get("annotations", [])

        if not original_annotations:
            print("No annotations found in JSON. Skipping.")
            continue

        img_to_anns = {}
        for ann in original_annotations:
            img_id = ann["image_id"]
            if img_id not in img_to_anns:
                img_to_anns[img_id] = []
            img_to_anns[img_id].append(ann)

        base_dir = os.path.dirname(json_path)
        all_img_ids = list(img_to_anns.keys())
        cat_name_to_id = {cat["name"]: cat["id"] for cat in coco_data.get("categories", [])}

        max_ann_id = max([ann.get("id", 0) for ann in original_annotations], default=0)

        new_annotations = []
        processed_image_ids = set()

        for i in tqdm(range(0, len(all_img_ids), batch_size)):
            batch_img_ids = all_img_ids[i : i + batch_size]

            batch_images = []
            batch_prompts = []
            batch_bboxes = []
            batch_labels = []
            batch_points = []
            batch_point_labels = []
            valid_batch_img_ids = []

            for img_id in batch_img_ids:
                img_info = images_dict[img_id]
                img_path = os.path.join(base_dir, img_info["file_name"])

                try:
                    pil_img = Image.open(img_path).convert("RGB")
                except Exception as e:
                    print(f"Failed to load image {img_path}: {e}")
                    continue

                anns = img_to_anns[img_id]
                img_w, img_h = img_info.get("width", 1), img_info.get("height", 1)

                img_boxes = []
                img_box_labels = []

                if click_seg:
                    batch_points.append([[[img_w / 2.0, img_h / 2.0]]])
                    batch_point_labels.append([[1]])

                for ann in anns:
                    bbox = ann.get("bbox")
                    if bbox:
                        x, y, w, h = bbox
                        if w >= img_w * 0.98 and h >= img_h * 0.98:
                            pass
                        else:
                            img_boxes.append([x, y, x + w, y + h])
                            img_box_labels.append(1)

                batch_images.append(pil_img)
                batch_prompts.append("leaf")
                valid_batch_img_ids.append(img_id)

                if not img_boxes:
                    batch_bboxes.append(None)
                    batch_labels.append(None)
                else:
                    batch_bboxes.append(img_boxes)
                    batch_labels.append(img_box_labels)

            if not batch_images:
                continue

            try:
                results = batch_inference(
                    model=model,
                    processor=processor,
                    device=device,
                    images=batch_images,
                    prompts=batch_prompts,
                    bboxes=batch_bboxes,
                    input_boxes_labels=batch_labels,
                    input_points=batch_points if click_seg else None,
                    input_points_labels=batch_point_labels if click_seg else None,
                    click_seg=click_seg,
                )
            except Exception as e:
                print(f"Batch inference failed: {e}")
                continue

            print(f"[DEBUG] len(results)={len(results)}")
            for img_idx, img_res in enumerate(results):
                print(f"[DEBUG] img_idx={img_idx}")
                print(f"[DEBUG] img_res={img_res}")

                current_img_id = valid_batch_img_ids[img_idx]
                masks = img_res["masks"]

                if len(masks) == 0:
                    continue

                processed_image_ids.add(current_img_id)

                np_masks = masks.cpu().numpy() if torch.is_tensor(masks) else masks
                img_info = images_dict[current_img_id]
                img_anns = img_to_anns[current_img_id]

                img_category_id = img_info.get("category_id")
                if img_category_id is None:
                    folder_name = img_info["file_name"].split("/")[0]
                    img_category_id = cat_name_to_id.get(folder_name)

                if img_category_id is None and len(img_anns) > 0:
                    img_category_id = img_anns[0].get("category_id")

                if img_category_id is None:
                    raise ValueError(
                        f"Not found category ID for the image at {os.path.join(base_dir, img_info['file_name'])}"
                    )

                print(f"[DEBUG] img_category_id={img_category_id}")
                print(f"[DEBUG] len(np_masks)={len(np_masks)}")
                print(f"[DEBUG] np_masks.shape={np_masks.shape}")

                img_cv2 = cv2.cvtColor(np.array(batch_images[img_idx]), cv2.COLOR_RGB2BGR)
                overlay_cv2 = img_cv2.copy()

                for j in range(len(np_masks)):
                    mask = np_masks[j]
                    polygons = mask_to_polygons(mask)

                    # print(f"[DEBUG] mask={mask}")
                    print(f"[DEBUG] mask.shape={mask.shape}")
                    # print(f"[DEBUG] polygons={polygons}")
                    print(f"[DEBUG] len(polygons)={len(polygons)}")

                    # ========================================================
                    # NDraw and save the overlaid masks
                    # ========================================================
                    if polygons:  # Only draw if polygons were successfully created
                        # 1. Generate a random color for this mask (BGR format)
                        color = np.random.randint(0, 255, (3,)).tolist()

                        # 2. Add a semi-transparent mask fill (50% opacity)
                        colored_mask = np.zeros_like(img_cv2)
                        colored_mask[mask > 0] = color
                        cv2.addWeighted(overlay_cv2, 1.0, colored_mask, 0.5, 0, dst=overlay_cv2)

                        # 3. Draw the solid polygon outlines
                        pts = [np.array(p, dtype=np.int32).reshape(-1, 1, 2) for p in polygons]
                        cv2.polylines(overlay_cv2, pts, isClosed=True, color=color, thickness=2)

                        # 4. Save the accumulated overlay image to a debug folder
                        debug_dir = os.path.join(base_dir, "debug_overlays")
                        os.makedirs(debug_dir, exist_ok=True)

                        # Flatten the subfolder structure in the filename so it saves safely
                        safe_filename = img_info["file_name"].replace("/", "_").replace("\\", "_")
                        save_path = os.path.join(debug_dir, f"overlay_{safe_filename}")

                        cv2.imwrite(save_path, overlay_cv2)
                    # ========================================================

                    if not polygons:
                        continue

                    y_indices, x_indices = np.where(mask > 0)
                    if len(x_indices) == 0 or len(y_indices) == 0:
                        continue

                    x_min, x_max = float(np.min(x_indices)), float(np.max(x_indices))
                    y_min, y_max = float(np.min(y_indices)), float(np.max(y_indices))
                    bbox = [x_min, y_min, x_max - x_min, y_max - y_min]

                    max_ann_id += 1
                    new_ann = {
                        "id": max_ann_id,
                        "image_id": current_img_id,
                        "category_id": img_category_id,
                        "segmentation": polygons,
                        "area": float(mask.sum()),
                        "bbox": bbox,
                        "iscrowd": 0,
                    }
                    new_annotations.append(new_ann)

        for old_ann in original_annotations:
            if old_ann["image_id"] not in processed_image_ids:
                new_annotations.append(old_ann)

        coco_data["annotations"] = new_annotations

        print(f"Saving updated annotations ({len(new_annotations)} total) to {json_path}")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(coco_data, f, separators=(",", ":"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SAM3 pseudo masks for dataset")
    parser.add_argument(
        "--dataset_dir",
        type=str,
        default="datasets/final",
        help="Path to dataset dir containing annotations.coco.json",
    )
    parser.add_argument("--batch_size", type=int, default=4, help="Batch size for SAM3 inference")
    parser.add_argument(
        "--click_seg",
        action="store_true",
        help="Use a single point (center of the image by default) to segment the image.",
    )
    args = parser.parse_args()

    if args.batch_size != 1 and args.click_seg:
        raise ValueError("Click Segmentation requires batch size = 1")

    device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}")

    process_dataset(args.dataset_dir, args.batch_size, device, args.click_seg)
