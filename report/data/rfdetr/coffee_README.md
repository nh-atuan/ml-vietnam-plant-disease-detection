# RF-DETR Segmentation - Coffee Plant Disease

Fine-tuned RF-DETR segmentation model for the `coffee` subset of the rice/coffee leaf disease dataset.

## Files

- `config.json`: model metadata and train config
- `class_names.json`: COCO category id to label mapping
- `metrics.csv`: evaluation metrics for this training run
- `best.pt`: best RF-DETR checkpoint

## Train Config

```json
{
  "name": "train_lr1e4",
  "model_size": "nano",
  "epochs": 8,
  "batch_size": 4,
  "grad_accum_steps": 4,
  "lr": 0.0001,
  "lr_encoder": 0.00015,
  "gradient_checkpointing": true,
  "early_stopping": true,
  "early_stopping_patience": 5
}
```

## Selected Metrics

| domain   | run         | name        | model_size   |   epochs |   batch_size |   grad_accum_steps |     lr |   lr_encoder | gradient_checkpointing   | early_stopping   |   early_stopping_patience |   mAP50_bbox |   mAP50_95_bbox |   mAP50_segm |   mAP50_95_segm |     mIoU |     Dice |   inference_ms_per_image |   num_eval_images | checkpoint                                                                     |
|:---------|:------------|:------------|:-------------|---------:|-------------:|-------------------:|-------:|-------------:|:-------------------------|:-----------------|--------------------------:|-------------:|----------------:|-------------:|----------------:|---------:|---------:|-------------------------:|------------------:|:-------------------------------------------------------------------------------|
| coffee   | train_lr1e4 | train_lr1e4 | nano         |        8 |            4 |                  4 | 0.0001 |      0.00015 | True                     | True             |                         5 |     0.819817 |        0.597979 |     0.842835 |        0.825083 | 0.857505 | 0.871758 |                  70.3064 |               576 | /kaggle/working/rf_detr_artifacts/coffee/train_lr1e4/checkpoint_best_total.pth |

## Data Notes

- Raw COCO annotations are used as the primary training source.
- Processed data is included as extra data when `USE_PROCESSED_EXTRA=1`; those records use pseudo full-image annotations because processed/ has no lesion COCO masks.
- Invalid/background labels such as `uit` are filtered before training.
