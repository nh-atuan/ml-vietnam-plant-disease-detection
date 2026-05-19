# YOLO26-seg Phase 3+4

Owner: Nguyen Ho Anh Tuan  
Task: Phase 3+4, item 3.2 in `docs/PLAN.md`

This folder contains the Kaggle notebook for training, evaluating, tuning, exporting, and uploading the YOLO26 segmentation model for the rice/coffee leaf disease dataset.

## Files

- `train_evaluate_tune.ipynb`: end-to-end Kaggle notebook.
- `README.md`: run notes, required outputs, and result template.

Large artifacts such as `.pt`, `.onnx`, TensorRT engines, and run folders must stay outside git. Upload the selected checkpoint and exported model to HuggingFace Hub instead.

## Taxonomy

The notebook uses the PLAN taxonomy and `models/class_names.json` order:

| id | class |
|---:|---|
| 0 | Healthy |
| 1 | BrownSpot |
| 2 | Hispa |
| 3 | LeafBlast |
| 4 | LeafMiner |
| 5 | PowderyMildew |
| 6 | Rust |
| 7 | AlgalLeafSpot |

Coffee labels are remapped from raw folder ids:

| raw folder | PLAN class |
|---|---|
| `0` | LeafMiner |
| `1` | PowderyMildew |
| `2` | Rust |
| `3` | AlgalLeafSpot |

The notebook intentionally does not trust `label_idx` from the current processed manifests because those metadata labels are not aligned with the PLAN taxonomy.

## Kaggle Run

1. Upload or attach the repository/dataset to Kaggle with:
   - `data/raw/rice_leaf_disease/annotations.coco.json`
   - `data/raw/coffee_leaf_disease/annotations.coco.json`
   - `data/processed/metadata/*_manifest.csv`
   - `models/class_names.json`
2. Open `train_evaluate_tune.ipynb`.
3. Set paths at the top if Kaggle mounts the dataset differently.
4. Run conversion and validation cells first.
5. Run the 3-epoch smoke test.
6. Run baseline and tuned experiments.
7. Set `HF_REPO_ID`, `HF_TOKEN`, and `HF_UPLOAD=1` only when ready to publish the final artifacts.

## Required Outputs

The completed Kaggle run must produce:

- YOLO segmentation dataset converted from COCO using fixed train/val/test manifests.
- At least 2 completed configs: baseline and tuned.
- Metrics: mask `mAP@50`, mask `mAP@50:95`, mIoU, Dice, inference ms/image, model size.
- At least 10 test visualizations with ground-truth vs prediction masks.
- Error-analysis examples, including `BrownSpot` vs `LeafBlast` and `AlgalLeafSpot` vs `Rust` when present.
- HuggingFace model repo link.

## Result Template

Fill this table after the Kaggle notebook has run.

| Run | Model | Epochs | imgsz | mAP@50 mask | mAP@50:95 mask | mIoU | Dice | Inference ms/img | Size MB |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline_yolo26n_seg | yolo26n-seg.pt | 50 | 640 | TBD | TBD | TBD | TBD | TBD | TBD |
| tuned_yolo26n_seg | yolo26n-seg.pt | 80 | 640 | TBD | TBD | TBD | TBD | TBD | TBD |

Best model: TBD  
HuggingFace Hub: TBD

