# Mask R-CNN ResNet50-FPN

Owner: Le Xuan Tri

This folder contains the Phase 3 Mask R-CNN baseline notebooks for plant disease instance segmentation. Both notebooks were executed on Kaggle GPU and include training, validation, tuning, test evaluation, visualization, error analysis, CPU inference benchmark, model export, and HuggingFace upload logs.

## Notebooks

| Domain | Notebook | HuggingFace model |
|---|---|---|
| Rice | `rice-mask-rcnn.ipynb` | https://huggingface.co/trisleex/mask-rcnn-rice-disease-model |
| Coffee | `coffee-mask-rcnn.ipynb` | https://huggingface.co/trisleex/mask-rcnn-coffee-disease-model |

## Final Test Results

| Domain | Config | mAP@50 | mAP@50:95 | mIoU | Dice | CPU ms/image | Size MB |
|---|---|---:|---:|---:|---:|---:|---:|
| Rice | Baseline | 0.128024 | 0.084388 | 0.680408 | 0.738192 | - | - |
| Rice | Tuned best | 0.182200 | 0.109017 | 0.552449 | 0.612051 | 569.70 | 501.73 |
| Coffee | Baseline | 0.680218 | 0.422597 | 0.726384 | 0.792677 | - | - |
| Coffee | Tuned best | 0.798665 | 0.591939 | 0.770262 | 0.823600 | 586.49 | 503.44 |

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
