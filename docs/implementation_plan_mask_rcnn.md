# Implementation Plan: Mask R-CNN ResNet50-FPN Baseline

## 1. Summary

This plan defines the Phase 3 and Phase 4 implementation protocol for the project baseline model: Mask R-CNN with a ResNet50-FPN backbone. The baseline must be stable, reproducible, and conservative so it can serve as a fair reference point for later segmentation models such as YOLO26-seg, RF-DETR, MobileSAM, and Mask2Former.

The implementation target is a Kaggle Notebook running on GPU T4 or P100. Training, validation, evaluation, tuning, error analysis, checkpoint export, and HuggingFace Hub preparation should be completed in one notebook and committed to:

```text
notebooks/models/mask_rcnn/train_evaluate_tune.ipynb
```

The final model artifacts should be prepared under Kaggle working storage and pushed to HuggingFace Hub because Kaggle input storage is read-only and notebook storage is non-persistent after the session.

## 2. Fixed Baseline Decisions

| Item | Decision |
|---|---|
| Model role | CNN-based baseline segmentation model |
| Implementation library | `torchvision.models.detection` |
| Architecture | Mask R-CNN ResNet50-FPN |
| Pretrained weights | Torchvision COCO-pretrained weights |
| Input size | `256x256`, matching Phase 2 preprocessing |
| Dataset format | COCO segmentation annotations |
| Dataset path on Kaggle | `/kaggle/input/<dataset-slug>/data/processed/...` |
| Number of project classes | 8 |
| Mask R-CNN classes | 9 including background |
| Main checkpoint metric | Validation `mAP@50:95` |
| Final test usage | Locked until final baseline/tuned evaluation |

Class order must follow `models/class_names.json`:

```text
0: Healthy
1: BrownSpot
2: Hispa
3: LeafBlast
4: LeafMiner
5: PowderyMildew
6: Rust
7: AlgalLeafSpot
```

For Mask R-CNN training, reserve model label id `0` for background and map project labels to ids `1..8`.

## 2.5. Model Architecture Overview

This section provides the theoretical background required by the course grading rubric (30% for "Chiều sâu lý thuyết"). The notebook must include a dedicated markdown section explaining Mask R-CNN before the training code.

### 2.5.1 ResNet50-FPN Backbone

The backbone is ResNet50 with a Feature Pyramid Network (FPN). ResNet50 extracts multi-scale feature maps from the input image through residual blocks at stages C2–C5. FPN then constructs a top-down pathway with lateral connections to produce feature maps P2–P5 at multiple resolutions. This multi-scale representation allows the model to detect objects of varying sizes, which is critical for leaf disease regions that range from small spots to large patches.

### 2.5.2 Region Proposal Network (RPN)

The RPN slides over the FPN feature maps and proposes candidate bounding boxes (anchors) that may contain objects. For each anchor, it predicts an objectness score (foreground vs background) and refines the bounding box coordinates. The RPN generates a set of region proposals that are passed to the next stages.

### 2.5.3 ROI Align

Unlike ROI Pooling, ROI Align uses bilinear interpolation to extract fixed-size feature maps from each proposed region without quantization artifacts. This preserves spatial precision, which is essential for accurate mask prediction at the pixel level.

### 2.5.4 Prediction Heads

Mask R-CNN has three parallel heads applied to each ROI:

- **Classification head:** predicts the disease class (1–8) or background (0).
- **Box regression head:** refines the bounding box coordinates.
- **Mask head:** predicts a binary mask for each class using a small FCN (fully convolutional network) that operates on the ROI-aligned features.

The mask head predicts one mask per class, and the final mask is selected based on the classification output. This decouples mask prediction from classification, which improves both tasks.

### 2.5.5 Why Mask R-CNN as Baseline

Mask R-CNN is chosen as the baseline because:

- It is the canonical two-stage instance segmentation model with well-understood behavior.
- `torchvision` provides a stable, well-tested implementation with COCO-pretrained weights.
- Its moderate complexity (compared to transformer-based models) makes it a fair reference for evaluating newer architectures like YOLO26-seg, RF-DETR, MobileSAM, and Mask2Former.
- Two-stage models typically achieve strong segmentation quality at the cost of inference speed, which sets clear expectations for the baseline vs advanced model comparison.

### 2.5.6 Loss Functions

Mask R-CNN optimizes a multi-task loss:

```text
L = L_cls + L_box + L_mask + L_objectness + L_rpn_box
```

where:

- `L_cls`: cross-entropy loss for ROI classification,
- `L_box`: smooth L1 loss for bounding box regression,
- `L_mask`: binary cross-entropy loss for mask prediction (per-pixel),
- `L_objectness`: binary cross-entropy for RPN foreground/background,
- `L_rpn_box`: smooth L1 for RPN box regression.

## 3. Kaggle Notebook Structure

The notebook should be structured with explicit sections:

1. Environment setup and imports.
2. Model architecture overview (theory section with markdown explanation).
3. Global seed and reproducibility setup.
4. Path configuration for Kaggle input and working output.
5. Dataset loading and COCO validation.
6. Transform and augmentation definitions.
7. DataLoader construction.
8. Model construction.
9. Baseline training with learning curves logging.
10. Baseline validation and checkpoint selection.
11. Learning curves visualization (train/val loss and metrics per epoch).
12. Baseline test evaluation.
13. Confusion matrix and classification-equivalent metrics.
14. Error analysis.
15. Tuning experiments.
16. Tuned model test evaluation.
17. Robustness evaluation (optional if time permits).
18. CPU inference benchmark and model size measurement.
19. HuggingFace export package preparation.
20. Final comparison table.

All major hyperparameters and file paths should be declared in a single configuration cell near the top of the notebook.

## 4. Reproducibility Protocol

The first executable notebook cell after imports must set a global seed, as required by `docs/MODEL_NOTES.md`.

Use `SEED = 42` unless a different seed is explicitly documented in the notebook.

The seed setup must cover:

- Python `random`.
- NumPy.
- PyTorch CPU RNG.
- PyTorch CUDA RNG.
- CUDA deterministic behavior.

Expected implementation behavior:

```python
def set_global_seed(seed: int = 42) -> None:
    import os
    import random
    import numpy as np
    import torch

    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

Record the seed in:

- notebook config,
- checkpoint metadata,
- HuggingFace `config.json`,
- model card.

For reproducibility verification, run a short smoke test with the same seed and confirm that the sampled batch order and initial mini-epoch losses are comparable.

## 5. Data Pipeline

### 5.1 Input Data

The notebook must consume the Phase 2 processed dataset in COCO format from:

```text
/kaggle/input/<dataset-slug>/data/processed/
```

The expected processed data includes:

- normalized or standardized `256x256` images,
- COCO annotation JSON files,
- train/validation/test split information,
- `normalization_stats.json`,
- preprocessing metadata such as `preprocessing_config.json` if available.

Do not recompute train normalization statistics in Phase 3. Load the train-only mean and standard deviation from:

```text
data/processed/metadata/normalization_stats.json
```

### 5.2 COCO Dataset Loader

Implement a custom PyTorch dataset that converts each COCO sample into the format expected by `torchvision` detection models.

Each `__getitem__` call must return:

```python
image, target
```

where `image` is:

```text
FloatTensor[3, 256, 256]
```

and `target` contains:

```python
{
    "boxes": FloatTensor[N, 4],     # xyxy format
    "labels": Int64Tensor[N],       # 1..8, background excluded
    "masks": UInt8Tensor[N, H, W],  # binary instance masks
    "image_id": Int64Tensor[1],
    "area": FloatTensor[N],
    "iscrowd": Int64Tensor[N],
}
```

COCO polygons must be rasterized into binary masks. Bounding boxes should be converted from COCO `xywh` to `xyxy`.

### 5.3 Dataset Validation

Before training, run validation checks and print a compact report:

- number of images per split,
- number of annotations per split,
- class distribution per split,
- number of dropped invalid annotations,
- number of images with zero valid instances,
- sample image size confirmation: `256x256`.

Invalid annotations should be skipped, not silently passed into training.

Drop or filter:

- boxes with width or height `<= 0`,
- empty masks,
- annotations with unknown category id,
- masks whose visible area is zero after rasterization.

If an image has no valid annotations after filtering, keep it only if the training/evaluation logic explicitly supports empty targets; otherwise exclude it and report the exclusion count.

### 5.4 Class Imbalance Handling

The Phase 2 pipeline produced a `WeightedRandomSampler` for addressing class imbalance. For Mask R-CNN with instance-level targets, the decision on whether to use weighted sampling must be explicitly documented in the notebook:

- If `WeightedRandomSampler` is used, compute image-level sample weights based on the rarest class annotation present in each image.
- If weighted sampling is not used, explain the rationale (e.g., Mask R-CNN handles imbalance through the RPN's positive/negative anchor ratio and the per-class mask head).
- Record the decision in the notebook config cell and checkpoint metadata.

## 6. Augmentation Pipeline

The plan distinguishes baseline-safe augmentation from tuning augmentation.

### 6.1 Baseline-Safe Augmentation

The baseline should stay vanilla and stable. Use moderate transforms that preserve annotation validity:

- horizontal flip,
- light affine transformation,
- light intensity transformation.

Suggested parameters:

- random horizontal flip probability: `0.5`,
- affine rotation: up to `+-15` degrees for baseline,
- translation: up to `0.05`,
- scale: `0.95..1.05`,
- brightness/contrast/saturation/hue jitter at low to moderate strength.

Validation and test transforms must be deterministic:

- image to tensor,
- normalization using `normalization_stats.json`.

### 6.2 Proposal Augmentation Requirements

The proposal requires:

- MixUp with `alpha = 0.4`,
- CutMix with `alpha = 1.0`,
- affine transformations,
- intensity transformations.

For Mask R-CNN, MixUp and CutMix are more complex than in classification because images, masks, boxes, and labels must remain consistent. Therefore:

- implement MixUp/CutMix as controlled training utilities,
- keep them out of the first vanilla baseline unless target merging is validated,
- introduce them in tuning experiments only,
- document the exact target-merging policy in the notebook.

When MixUp or CutMix is enabled, the implementation must:

- transform images and masks together,
- merge target dictionaries from both source samples,
- recompute boxes from transformed masks where needed,
- drop boxes/masks that become empty,
- log the augmentation probability and alpha value.

If MixUp target semantics are judged too noisy for instance segmentation, keep MixUp as an ablation marked "experimental" and prefer CutMix for mask-preserving augmentation.

## 7. Baseline Setup

This section is the strict reference implementation. It should be completed before any tuning experiment.

### 7.1 Model

Use:

```python
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.mask_rcnn import MaskRCNNPredictor
```

Initialize:

```python
model = maskrcnn_resnet50_fpn(weights="DEFAULT")
```

Replace the prediction heads:

- box classification head: `num_classes = 9`,
- mask prediction head: `num_classes = 9`.

Keep the ResNet50-FPN backbone unchanged for the baseline.

### 7.2 Training Defaults

Recommended baseline config:

| Hyperparameter | Baseline value |
|---|---|
| Epochs | 20 |
| Batch size | 2 |
| Optimizer | AdamW |
| Learning rate | `1e-4` |
| Weight decay | `1e-4` |
| Scheduler | ReduceLROnPlateau or cosine schedule |
| Early stopping patience | 5 epochs |
| Score threshold for visualization | `0.5` |
| Device | CUDA if available |

Use gradient clipping if losses become unstable:

```text
max_norm = 5.0
```

The baseline should not use architecture changes, heavy augmentation, or custom post-processing beyond standard Mask R-CNN outputs.

### 7.3 Training Loop

For each epoch:

1. Set `model.train()`.
2. Iterate over train DataLoader.
3. Move images and targets to device.
4. Compute Mask R-CNN loss dictionary.
5. Sum all losses.
6. Backpropagate.
7. Apply gradient clipping if enabled.
8. Step optimizer.
9. Log train loss components:
   - classifier loss,
   - box regression loss,
   - mask loss,
   - objectness loss,
   - RPN box regression loss,
   - total loss.
10. Run validation evaluation.
11. Save last checkpoint.
12. Save best checkpoint if validation `mAP@50:95` improves.
13. Update scheduler and early stopping state.
14. Record epoch-level metrics to a history list for learning curves.

All checkpoints must be written to:

```text
/kaggle/working/mask_rcnn_runs/
```

### 7.4 Checkpoint Contents

Each checkpoint should contain:

```python
{
    "model_state_dict": ...,
    "optimizer_state_dict": ...,
    "scheduler_state_dict": ...,
    "epoch": ...,
    "best_metric": ...,
    "class_names": ...,
    "class_to_model_id": ...,
    "input_size": [256, 256],
    "normalization_stats": ...,
    "seed": 42,
    "config": ...,
    "metrics": ...,
}
```

The best baseline checkpoint should be named:

```text
mask_rcnn_resnet50_fpn_baseline_best.pth
```

### 7.5 Learning Curves

After training completes, the notebook must plot learning curves as required by the proposal (§6.1):

- **Loss curves:** train total loss and validation total loss per epoch on the same plot.
- **Individual loss components:** classifier loss, box loss, mask loss per epoch (train only).
- **Validation metric curve:** `mAP@50:95` per epoch.
- **Mark best epoch:** annotate the epoch at which the best checkpoint was saved.

These plots help observe overfitting behavior and training stability, and are required content for the final report.

## 8. Evaluation Metrics

Evaluation must use the same validation and test protocol across all reported configurations.

### 8.1 Core Segmentation Metrics

Report:

- `mAP@50`,
- `mAP@50:95`,
- `mIoU`,
- Dice Score.

Use COCO-style evaluation for mAP when possible. If a custom evaluator is used, document:

- IoU thresholds,
- matching strategy,
- confidence threshold,
- whether metrics are macro-averaged across classes or averaged across instances.

### 8.2 Classification-Equivalent Metrics

To maintain consistency with the project proposal (which defines Macro F1 as the primary metric for the overall project comparison), the notebook must also report classification-equivalent metrics derived from matched detection predictions:

- **Macro F1-score:** computed from per-class Precision and Recall of matched predictions.
- **Weighted F1-score:** weighted by class support to account for imbalance.
- **Accuracy:** fraction of correctly classified matched detections.

For each matched prediction (IoU ≥ 0.5 with a ground-truth instance), record the predicted class and ground-truth class. From these matched pairs, compute a standard multi-class confusion matrix and derive F1 scores.

Note: `mAP@50:95` remains the primary metric for checkpoint selection within this notebook. Macro F1 is reported for cross-model comparison with other project models.

### 8.3 Confusion Matrix

The notebook must produce confusion matrices for test set predictions:

- **Absolute count matrix:** 8×8 (project classes only, excluding background).
- **Row-normalized matrix:** each row sums to 1.0, showing per-class recall distribution.
- **Visualization:** heatmap with annotated cell values.
- **Highlight top confused pairs:** specifically annotate `BrownSpot↔LeafBlast` and `AlgalLeafSpot↔Rust`.

Matching protocol for confusion matrix entries:

1. For each ground-truth instance, find the highest-IoU predicted instance with IoU ≥ 0.5.
2. If matched, record (GT class, predicted class).
3. If unmatched (false negative), record as missed for that GT class.
4. Predicted instances with no GT match (false positives) are recorded separately.

### 8.4 Per-Class And Domain-Level Metrics

Report metrics:

- overall,
- per class (Precision, Recall, F1, AP, IoU for each of the 8 classes),
- per domain: **rice-only** and **coffee-only** subsets (this is mandatory since domain metadata is available from Phase 1).

The per-class report is required because the dataset has class imbalance and visually similar disease pairs.

The per-domain report must include at least `mAP@50:95` and `Macro F1` for each domain to evaluate cross-domain generalization.

### 8.5 Per-Class Precision-Recall Curves

Plot Precision-Recall curves for each of the 8 project classes:

- One subplot or overlaid plot showing all 8 classes.
- Annotate the AP value for each class in the legend.
- Highlight classes with AP below 0.5 for targeted improvement discussion.

This replaces the proposal's ROC one-vs-rest requirement, which is more natural for classification. PR curves are the standard equivalent for detection and segmentation models.

### 8.6 Business And Application Metrics

Measure:

- CPU inference time in milliseconds per image,
- throughput in images per second (computed as `1000 / mean_ms`),
- model size in MB.

CPU inference benchmark protocol:

1. Load best checkpoint on CPU.
2. Set `model.eval()`.
3. Use batch size `1`.
4. Run at least 10 warm-up images.
5. Measure at least 100 images or the full test set if smaller.
6. Report mean, standard deviation, median, p95 if practical.
7. Report throughput as images per second.

Model size protocol:

- measure `.pth` checkpoint size in MB,
- optionally measure export package size after compression.

### 8.7 Robustness Evaluation (Optional)

If Kaggle GPU time permits, evaluate model robustness against test-time perturbations as requested by the proposal (§6.1):

1. **Brightness jitter:** apply ±10% brightness change to test images and re-evaluate.
2. **Gaussian blur:** apply Gaussian blur with σ=1.0 and re-evaluate.
3. **Contrast shift:** apply ±10% contrast change and re-evaluate.

Report the `mAP@50:95` drop for each perturbation type. This helps assess model reliability for real-world agricultural field conditions.

If time is insufficient, mark this section as "deferred" and note it as a known limitation.

### 8.8 Calibration Analysis (Optional)

If time permits, analyze the calibration of prediction confidence scores:

- **Reliability diagram:** plot predicted confidence vs actual accuracy.
- **Expected Calibration Error (ECE):** quantify calibration quality.
- **Interpretation:** note whether confidence scores are trustworthy for the web application's user-facing display.

This is requested by the proposal (§6.4) to ensure confidence values shown to farmers are meaningful.

## 9. Error Analysis

Error analysis is required for the baseline, not optional. It should be run after baseline test evaluation and repeated for the best tuned model if time permits.

### 9.1 Required Error Groups

Analyze failures according to the four proposal groups:

1. Visual similarity between diseases.
2. Low-quality images, including blur, poor lighting, low contrast, or strong shadows.
3. Complex compositions, including multiple leaves, occlusion, cluttered backgrounds, or overlapping regions.
4. Healthy vs. early-stage disease confusion.

### 9.2 Known High-Risk Pairs

Pay special attention to:

- `BrownSpot` vs `LeafBlast`,
- `AlgalLeafSpot` vs `Rust`,
- `Healthy` vs early-stage disease samples.

### 9.3 Required Outputs

Save and display:

- at least 10 test predictions with ground-truth masks and predicted masks,
- top false positives by confidence,
- top false negatives by missed ground-truth area,
- examples grouped by the four error categories,
- a short written diagnosis for each group.

Each error category should include:

- representative image ids,
- ground-truth label,
- predicted label,
- confidence,
- IoU or Dice,
- likely cause,
- suggested improvement for later models or tuning.

## 10. Tuning Experiments

This section must be separate from the Baseline Setup. Tuning starts only after the vanilla baseline has produced a valid checkpoint and full validation report.

### 10.1 Tuning Principles

Tuning must remain conservative:

- keep Mask R-CNN ResNet50-FPN,
- do not migrate to Detectron2 or MMDetection,
- do not change the dataset split,
- do not use the test set for trial selection,
- compare every tuned run against the vanilla baseline.

### 10.2 Experiment Matrix

Run at least two tuning configurations, as required by the project plan.

Recommended tuning experiments:

| Experiment | Change | Values |
|---|---|---|
| A | Learning rate | `5e-5`, `1e-4`, `3e-4` |
| B | Effective batch size | `2`, `4` using gradient accumulation if needed |
| C | Augmentation strength | light baseline vs stronger affine/intensity |
| D | CutMix | off vs `alpha=1.0` |
| E | MixUp | off vs `alpha=0.4`, experimental |

If Kaggle GPU time is limited, prioritize:

1. learning rate,
2. effective batch size,
3. CutMix.

### 10.3 Tuning Selection Rule

Select the best tuned model by validation `mAP@50:95`.

Use these as secondary criteria:

- `mAP@50`,
- `mIoU`,
- Dice Score,
- CPU inference time,
- model size,
- train/validation loss gap.

Only after selecting the best tuned checkpoint should the notebook evaluate it on the locked test split.

### 10.4 Final Comparison Table

The notebook must produce a final comparison table:

| Config | mAP@50 | mAP@50:95 | mIoU | Dice | Macro F1 | CPU ms/image | img/s | Size MB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | - | - | - | - | - | - | - | - |
| Tuned best | - | - | - | - | - | - | - | - |

Add notes explaining whether tuning improved segmentation quality, only improved localization, or increased overfitting.

Include a secondary per-domain comparison if applicable:

| Config | Domain | mAP@50:95 | Macro F1 |
|---|---|---:|---:|
| Baseline | Rice | - | - |
| Baseline | Coffee | - | - |
| Tuned best | Rice | - | - |
| Tuned best | Coffee | - | - |

## 11. HuggingFace Hub Export

Kaggle storage is non-persistent, so the notebook must prepare model artifacts for upload before the session ends.

Create:

```text
/kaggle/working/hf_export/
```

Required files:

```text
hf_export/
  pytorch_model.pth
  config.json
  class_names.json
  normalization_stats.json
  README.md
```

The HuggingFace model card should include:

- project name,
- model architecture,
- baseline role,
- library and version,
- input size `256x256`,
- dataset description,
- class list,
- seed,
- train/validation/test split policy,
- metrics table,
- CPU inference time,
- model size,
- known limitations,
- four-group error analysis summary.

The notebook should include a final upload cell using `huggingface_hub`. The token must be provided through Kaggle Secrets, not hard-coded.

## 12. Acceptance Criteria

The implementation is complete when all of the following are true:

- The notebook includes a model architecture overview section explaining Mask R-CNN theory.
- The notebook sets a global seed before training.
- The model is Mask R-CNN ResNet50-FPN from `torchvision`.
- Input images are handled as `256x256`.
- The dataset is loaded from processed COCO annotations.
- The notebook uses 8 project classes plus background.
- `normalization_stats.json` is loaded and recorded.
- The class imbalance handling strategy (WeightedRandomSampler or alternative) is documented.
- The vanilla baseline trains successfully and saves a best checkpoint.
- Learning curves (loss and metrics per epoch) are plotted.
- Validation and test metrics include `mAP@50`, `mAP@50:95`, `mIoU`, and Dice Score.
- Classification-equivalent metrics include Macro F1, Weighted F1, and Accuracy.
- Confusion matrix (absolute and normalized) is produced.
- Per-class Precision, Recall, F1, and AP are reported for all 8 classes.
- Per-class Precision-Recall curves are plotted.
- Per-domain metrics (rice vs coffee) are reported.
- CPU inference time, throughput, and model size are reported.
- Error analysis covers all four required groups.
- Tuning experiments are clearly separated from the baseline setup.
- Best checkpoint and metadata are prepared for HuggingFace Hub.
- The notebook output includes visual predictions and a final baseline vs tuned comparison table.

## 13. Test Plan

### 13.1 Dataset Tests

- Load all COCO files without missing images.
- Verify every category maps to one of the 8 known classes.
- Verify all returned boxes are valid `xyxy`.
- Verify masks are binary and match the image size.
- Visualize at least 5 random train samples with boxes and masks.

### 13.2 Training Tests

- Run a one-batch forward pass.
- Run a one-batch backward pass.
- Confirm all loss values are finite.
- Run a mini training epoch on a small subset before full training.
- Confirm checkpoint save and reload work.

### 13.3 Evaluation Tests

- Run validation evaluation on a small subset.
- Confirm metric values are within valid ranges.
- Confirm prediction masks align with the original `256x256` coordinate system.
- Confirm per-class metric tables include all 8 project classes.

### 13.4 Reproducibility Tests

- Run the same mini training subset twice with the same seed.
- Confirm sampled order and early losses are comparable.
- Record any unavoidable nondeterminism from CUDA operations.

### 13.5 Artifact Tests

- Reload the best checkpoint on CPU.
- Run inference on one test image.
- Verify HuggingFace export folder contains all required files.
- Verify `config.json` and model card match the actual notebook config.

## 14. Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Kaggle session ends before upload | Save best artifacts continuously to `/kaggle/working/` and push to HuggingFace immediately after training |
| GPU memory error | Start with batch size 2 and use gradient accumulation for larger effective batch size |
| Invalid COCO polygons | Validate and filter annotations before training |
| MixUp/CutMix corrupts instance targets | Keep them out of the vanilla baseline and enable only as documented tuning ablations |
| Overfitting due to small dataset | Use validation checkpointing, early stopping, moderate augmentation, and per-class analysis |
| Test leakage | Use validation only for tuning and lock test until final evaluation |
| Slow CPU inference | Report honestly as a business metric; optimization belongs to later ONNX/export phase |

## 15. Final Deliverables

Expected repository deliverables:

```text
notebooks/models/mask_rcnn/train_evaluate_tune.ipynb
notebooks/models/mask_rcnn/README.md
```

Expected Kaggle/HuggingFace artifacts:

```text
mask_rcnn_resnet50_fpn_baseline_best.pth
mask_rcnn_resnet50_fpn_tuned_best.pth
config.json
class_names.json
normalization_stats.json
README.md
```

The `README.md` in the model folder should include:

- Kaggle notebook link,
- HuggingFace model link,
- final metric table,
- CPU inference time,
- model size,
- key error analysis findings,
- known limitations.
