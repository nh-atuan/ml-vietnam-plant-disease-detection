# Mask2Former — VN Plant Disease Segmentation

**Tác giả:** Dương Tuấn Anh (23120208)
**Task:** 3.5 (Phase 3+4) + Sáng tạo S2
**Status:** 🚧 In progress — chờ chạy trên Kaggle

## Mục tiêu

Fine-tune Mask2Former (Transformer-based universal segmentation, SOTA trên COCO) trên dataset lá lúa & cà phê Việt Nam, so sánh với 4 model còn lại (Mask R-CNN, YOLO26-seg, RF-DETR, MobileSAM).

## Notebooks

| File | Domain | Classes | Dataset path |
|------|--------|---------|--------------|
| `train_evaluate_tune_rice.ipynb` | Lúa (Rice) | BrownSpot, Healthy, Hispa, LeafBlast | `rice_leaf_disease/` |
| `train_evaluate_tune_coffee.ipynb` | Cà phê (Coffee) | LeafMiner, PowderyMildew, Rust, AlgalLeafSpot | `coffee_leaf_disease/` |

> `train_evaluate_tune.ipynb` — skeleton gốc (tham khảo, không dùng để nộp)

## Setup trên Kaggle

### 1. Thêm Dataset

Trên Kaggle Notebook → **Add Data** → tìm `magnusdtd2/rice-coffee-leaf-disease`.

Dataset sẽ mount tại:
```
/kaggle/input/rice-coffee-leaf-disease/
├── rice_leaf_disease/
│   ├── train/       (ảnh train)
│   ├── val/         (ảnh val)
│   ├── test/        (ảnh test)
│   ├── train.coco.json
│   ├── val.coco.json
│   └── test.coco.json
└── coffee_leaf_disease/
    ├── train/
    ├── val/
    ├── test/
    ├── train.coco.json
    ├── val.coco.json
    └── test.coco.json
```

> **⚠️ Verify paths:** Sau khi Add Data, mở file manager Kaggle để xác nhận cấu trúc thực tế rồi điều chỉnh `DATA_ROOT`, `TRAIN_JSON`, v.v. trong cell cấu hình nếu cần.

### 2. Kaggle Secrets

Thêm secret:
- `HUGGINGFACE_TOKEN` — HF token có quyền write để push checkpoint

### 3. Notebook settings

- Accelerator: **GPU P100** (ưu tiên) hoặc **T4 x2**
- Internet: **ON** (cần pull pretrained weights từ HF Hub)
- Persistence: Files only

## Hyperparameter tuning (mỗi notebook)

| # | Config | Backbone | Image size | Batch | LR | Augmentation |
|---|--------|----------|-----------|-------|-----|--------------|
| 1 | `run1_baseline` | Mask2Former Swin-T | 384 | 4 | 5e-5 | light |
| 2 | `run2_tuned` | Mask2Former Swin-S | 512 | 2 | 1e-4 | strong |

## Augmentation (theo PLAN.md dòng 96)

| Technique | Implementation |
|-----------|----------------|
| **Affine** | `A.Affine(scale, translate, rotate, shear)` |
| **Intensity Transformation** | `A.RandomBrightnessContrast`, `A.HueSaturationValue` |
| **CutOut** | `A.CoarseDropout(max_holes=8)` |
| **CutMix** | `apply_cutmix_pixels()` — batch-level |
| **Mixup** | Có thể áp dụng bổ sung ở batch level |

## Metrics

Tính bằng `torchmetrics.detection.MeanAveragePrecision(iou_type='segm')` + manual IoU/Dice:

| Metric | Mô tả |
|--------|-------|
| mAP@50 | Instance segmentation AP tại IoU=0.50 |
| mAP@50:95 | AP trung bình từ IoU=0.50 đến 0.95 (COCO standard) |
| mIoU | Mean Intersection over Union per instance |
| Dice | Dice coefficient per instance |
| Inference time | ms/ảnh trên GPU |

## Kết quả

> Sẽ điền sau khi chạy xong trên Kaggle.

### Rice (lúa)

| Run | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) |
|-----|--------|-----------|------|------|----------------|
| `run1_baseline` (Swin-T, 384) | TBD | TBD | TBD | TBD | TBD |
| `run2_tuned` (Swin-S, 512) | TBD | TBD | TBD | TBD | TBD |

### Coffee (cà phê)

| Run | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) |
|-----|--------|-----------|------|------|----------------|
| `run1_baseline` (Swin-T, 384) | TBD | TBD | TBD | TBD | TBD |
| `run2_tuned` (Swin-S, 512) | TBD | TBD | TBD | TBD | TBD |

## HuggingFace Hub

> Sẽ cập nhật link sau khi push.

| Domain | HF Repo | Load code |
|--------|---------|-----------|
| Rice | `vn-plant-disease/mask2former-rice-seg` | `Mask2FormerForUniversalSegmentation.from_pretrained(...)` |
| Coffee | `tunah/mask2former-coffee-seg` | `Mask2FormerForUniversalSegmentation.from_pretrained(...)` |

## Đóng góp Sáng tạo S2

Mask2Former là **Transformer-based universal segmentation** đạt SOTA trên COCO. Điểm nổi bật:

- Cùng một kiến trúc giải quyết semantic + instance + panoptic segmentation
- Masked attention trong pixel decoder — tập trung vào foreground objects
- Fine-tune trên 2 domain độc lập (rice + coffee) — cho phép so sánh cross-domain

**Đóng góp học thuật:** So sánh Mask2Former (Transformer) với Mask R-CNN (CNN baseline) trên cùng dataset lá VN, đánh giá trade-off accuracy vs inference speed.

## Error analysis

> Sẽ viết sau khi có kết quả thực.

Câu hỏi cross-domain:
1. Domain nào khó hơn (rice hay coffee)?
2. Class nào có mIoU thấp nhất ở mỗi domain?
3. Aug `strong` có consistently giúp cả 2 domain không?

## TODO trước khi nộp

- [ ] Chạy cả 2 notebooks trên Kaggle (capture full output)
- [ ] Điền bảng metrics (rice + coffee)
- [ ] Push checkpoints lên HF, cập nhật links
- [ ] Viết error analysis cells (2 notebooks)
- [ ] Visualize ≥ 10 ảnh/notebook (pred vs GT)
- [ ] Gửi metrics cho Tống Phúc (task 3.6 — bảng so sánh 5 model)
- [ ] Commit `.ipynb` đã có output vào repo
