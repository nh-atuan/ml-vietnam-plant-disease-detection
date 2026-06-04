# YOLO26-seg Phase 3

Owner: Nguyen Ho Anh Tuan  
Task: Phase 3, item 3.2 in `docs/PLAN.md`

This folder contains the Kaggle notebooks for training, evaluating, and uploading the YOLO26 segmentation model separately for the rice and coffee leaf disease datasets.

## Files

- `train_eval_rice.ipynb`: Phase 3 Kaggle notebook for the Rice dataset.
- `train_eval_coffee.ipynb`: Phase 3 Kaggle notebook for the Coffee dataset.
- `train_evaluate_tune.ipynb`: old combined Phase 3+4 notebook kept only as a reference.
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
2. Open `train_eval_rice.ipynb` or `train_eval_coffee.ipynb`.
3. Set paths at the top if Kaggle mounts the dataset differently.
4. Run conversion and validation cells first.
5. Run the 1-epoch smoke test.
6. Run Phase 3 baseline training and evaluation.
7. Set `HF_REPO_ID`, `HF_TOKEN`, and `HF_UPLOAD=1` only when ready to publish the final artifacts.

## Required Outputs

The completed Kaggle run must produce:

- YOLO segmentation dataset converted from COCO using fixed train/val/test manifests.
- One completed Phase 3 baseline run per dataset notebook.
- Metrics: mask `mAP@50`, mask `mAP@50:95`, mIoU, Dice, inference ms/image, model size.
- At least 10 test visualizations with ground-truth vs prediction masks.
- Error-analysis examples, including `BrownSpot` vs `LeafBlast` and `AlgalLeafSpot` vs `Rust` when present.
- HuggingFace model repo link.

## Result Template

Fill this table after the Kaggle notebook has run.

| Run | Model | Epochs | imgsz | mAP@50 mask | mAP@50:95 mask | mIoU | Dice | Inference ms/img | Size MB |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| phase3_yolo26n_seg_rice | yolo26n-seg.pt | 50 | 640 | TBD | TBD | TBD | TBD | TBD | TBD |
| phase3_yolo26n_seg_coffee | yolo26n-seg.pt | 50 | 640 | TBD | TBD | TBD | TBD | TBD | TBD |

Best model: TBD  
HuggingFace Hub: TBD

