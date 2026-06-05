# Mask R-CNN ResNet50-FPN

Owner: Le Xuan Tri

This folder contains the Phase 3 Mask R-CNN baseline notebooks for plant disease instance segmentation. Both notebooks were executed on Kaggle GPU and include training, validation, tuning, test evaluation, visualization, error analysis, CPU inference benchmark, model export, and HuggingFace upload logs.

## Notebooks

| Domain | Notebook | HuggingFace model |
|---|---|---|
| Rice | `rice-mask-rcnn.ipynb` | https://huggingface.co/trisleex/mask-rcnn-rice-disease-model |
| Coffee | `coffee-mask-rcnn.ipynb` | https://huggingface.co/trisleex/mask-rcnn-coffee-disease-model |

## Final Test Results

| Model Type | mAP@50 | mAP@50:95 | mIoU | Dice | Accuracy | Inference (ms) | Throughput (img/s) | Size (MB) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Rice Mask R-CNN (Baseline) | 0.596557 | 0.529380 | 0.866922 | 0.893484 | 0.099948 | 760.50 | 1.3149 | 503.44 |
| Rice Mask R-CNN (Tuned best) | 0.540375 | 0.480468 | 0.870831 | 0.899939 | 0.031775 | 760.50 | 1.3149 | 503.44 |
| Coffee Mask R-CNN (Baseline) | 0.947967 | 0.904079 | 0.912823 | 0.935618 | 0.525223 | 702.36 | 1.4238 | 501.73 |
| Coffee Mask R-CNN (Tuned best) | 0.919455 | 0.859970 | 0.897318 | 0.922537 | 0.278725 | 702.36 | 1.4238 | 501.73 |

## Stage 3 Coverage

- Model: Mask R-CNN ResNet50-FPN, CNN-based baseline.
- Dataset: Phase 2 processed COCO splits mounted in Kaggle.
- Training flow: load data, augment, train, validate, evaluate, tune, export.
- Metrics: mAP@50, mAP@50:95, mIoU, Dice, Macro F1, Weighted F1, Accuracy, CPU latency, throughput, model size.
- Visual checks: prediction masks versus ground truth on 10 test images, PR curves, and row-normalized confusion matrix.
- Tuning: multiple LR, batch/effective batch, CutMix, strong augmentation, and frozen-backbone configurations.
- Checkpoint selection: validation mAP@50:95.

## Kaggle Requirements

- Mount the processed dataset under `/kaggle/input/.../data/processed`.
- Keep class names and normalization metadata available from the processed dataset or embedded notebook fallback.
- Store HuggingFace token in Kaggle Secrets as `HF_TOKEN`; do not hard-code tokens.

## HuggingFace Export Package

Each notebook exports:

```text
hf_export/
  pytorch_model.pth
  config.json
  class_names.json
  normalization_stats.json
  export_manifest.json
  README.md
```
