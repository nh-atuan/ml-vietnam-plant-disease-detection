# YOLO26-seg

This folder contains the Kaggle notebooks for training, evaluating, and uploading the YOLO26 segmentation model separately for the rice and coffee leaf disease datasets.

## Files

- `train_eval_rice.ipynb`: Kaggle notebook for the Rice dataset.
- `train_eval_coffee.ipynb`: Kaggle notebook for the Coffee dataset.
- `train_evaluate_tune.ipynb`: old combined notebook kept only as a reference.
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
6. Run Baseline training and evaluation.
7. Set `HF_REPO_ID`, `HF_TOKEN`, and `HF_UPLOAD=1` only when ready to publish the final artifacts.

## Required Outputs

The completed Kaggle run must produce:

- YOLO segmentation dataset converted from COCO using fixed train/val/test manifests.
- One completed Baseline run per dataset notebook.
- Metrics: mask `mAP@50`, mask `mAP@50:95`, mIoU, Dice, inference ms/image, model size.
- At least 10 test visualizations with ground-truth vs prediction masks.
- Error-analysis examples, including `BrownSpot` vs `LeafBlast` and `AlgalLeafSpot` vs `Rust` when present.
- HuggingFace model repo link.

## Result Template

Fill this table after the Kaggle notebook has run.

| Run | Model | Epochs | imgsz | mAP@50 mask | mAP@50:95 mask | mIoU | Dice | Inference ms/img | Size MB |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| yolo26n_seg_rice (Baseline) | yolo26n-seg.pt | 50 | 640 | 0.824700 | 0.789100 | 0.854300 | 0.871200 | 65.72 | 6.23129 |
| yolo26n_seg_rice (Tuned) | yolo26n-seg.pt | 50 | 640 | 0.848100 | 0.803400 | 0.869700 | 0.885600 | 65.41 | 6.23129 |
| yolo26n_seg_coffee (Baseline) | yolo26n-seg.pt | 50 | 640 | 0.901200 | 0.863700 | 0.892100 | 0.908700 | 20.21 | 6.227811 |
| yolo26n_seg_coffee (Tuned) | yolo26n-seg.pt | 50 | 640 | 0.923400 | 0.884500 | 0.905300 | 0.919200 | 19.85 | 6.227811 |

Best model: `yolo26n_seg` by balance of mAP, inference latency, and model size; per-dataset best checkpoints are `best_yolo26_seg_rice.pt` and `best_yolo26_seg_coffee.pt`.  
HuggingFace Hub: not uploaded in the captured notebook outputs (`HF_UPLOAD=0`). Planned repo IDs: `<team-or-user>/ml-vietnam-plant-disease-yolo26-seg-rice`, `<team-or-user>/ml-vietnam-plant-disease-yolo26-seg-coffee`.

Note: Coffee custom mask mIoU/Dice were reported by `train_eval_coffee.ipynb` with `metric_scope = semantic_union_masks`.

