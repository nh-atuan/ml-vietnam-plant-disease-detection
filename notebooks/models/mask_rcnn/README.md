# Mask R-CNN ResNet50-FPN Baseline

Notebook:

```text
notebooks/models/mask_rcnn/train_evaluate_tune.ipynb
```

Purpose:

- Train the project baseline instance segmentation model.
- Evaluate overall and per-domain Rice/Coffee performance.
- Report mAP@50:95, mAP@50, mIoU, Dice, Macro F1, Weighted F1, Accuracy, PR curves, and row-normalized confusion matrix.
- Run conservative tuning experiments after the vanilla baseline.
- Prepare HuggingFace Hub artifacts from Kaggle working storage.

Kaggle expectations:

- Mount the Phase 2 processed dataset at `/kaggle/input/<dataset-slug>/data/processed/...`.
- Keep `models/class_names.json` available or verify the embedded fallback class order.
- Store HuggingFace token in Kaggle Secrets as `HF_TOKEN`; do not hard-code tokens.

Primary checkpoint criterion:

```text
validation mAP@50:95
```

Required export package:

```text
hf_export/
  pytorch_model.pth
  config.json
  class_names.json
  normalization_stats.json
  README.md
```
