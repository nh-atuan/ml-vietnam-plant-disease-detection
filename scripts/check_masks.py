import json
import os
import sys


def check_coco_masks(json_path):
    """
    Checks a COCO annotation file for images that are missing segmentation masks.
    """
    if not os.path.exists(json_path):
        print(f"Error: File not found at {json_path}")
        return

    print(f"Reading {json_path}...")
    try:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
    except MemoryError:
        print("Error: Out of memory. The annotation file is too large for standard json.load().")
        print("Please use a machine with more RAM or a streaming parser implementation.")
        return
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    images = {img["id"]: img["file_name"] for img in data.get("images", [])}
    annotations = data.get("annotations", [])

    # Track distinct image IDs that have at least one non-empty segmentation
    images_with_masks = set()
    for ann in annotations:
        image_id = ann.get("image_id")
        seg = ann.get("segmentation")

        has_mask = False
        if isinstance(seg, list):
            if len(seg) > 0:
                has_mask = True
        elif isinstance(seg, dict):
            if seg.get("counts"):
                has_mask = True

        if has_mask:
            images_with_masks.add(image_id)

    all_image_ids = set(images.keys())
    missing_mask_ids = all_image_ids - images_with_masks

    print("-" * 30)
    print(f"Total images in dataset:      {len(all_image_ids)}")
    print(f"Images with at least one mask: {len(images_with_masks)}")
    print(f"Images missing masks:         {len(missing_mask_ids)}")
    print("-" * 30)

    if missing_mask_ids:
        print("\nExample images missing masks:")
        sorted_missing = sorted(list(missing_mask_ids))
        for img_id in sorted_missing:
            print(f" - ID {img_id}: {images.get(img_id, 'Unknown filename')}")
        print(f"There is a total of {len(missing_mask_ids)} missing images.")
    else:
        print("\nSuccess: All images have at least one segmentation mask!")


if __name__ == "__main__":
    target_file = "datasets/final/coffee_leaf_disease/annotations.coco.json"

    if len(sys.argv) > 1:
        target_file = sys.argv[1]

    check_coco_masks(target_file)
