# Experiments — Tổng quan

Thư mục chứa toàn bộ thực nghiệm huấn luyện cho từng mô hình.

## Cấu trúc

| Thư mục | Mô hình | Phụ trách | Phase |
|---------|---------|-----------|-------|
| `mobilenetv2/` | MobileNetV2 (baseline nhẹ) | Lê Xuân Trí | 3–4 |
| `resnet50/` | ResNet50 (baseline mạnh) | Đàm Tiến Đạt | 3–4 |
| `swin_transformer/` | Swin Transformer | Tống Thanh Phúc | 3–4 |
| `dinov3/` | DINOv3 fine-tune *(sáng tạo)* | Dương Tuấn Anh | 3–4 |

## Quy ước chung
- Config YAML riêng cho mỗi model: `configs/models/<model>.yaml`
- Shared defaults: `configs/training_defaults.yaml`
- Entry point: `experiments/<model>/train.py --config configs/models/<model>.yaml`
- Checkpoints lưu tại: `experiments/<model>/checkpoints/`
- Tuning results: `experiments/<model>/tuning/`
- Tất cả runs log lên MLflow

## Workflow
1. **Phase 3**: Baseline run → log MLflow
2. **Phase 4**: Hyperparameter tuning (random search → Ray Tune) → best config → re-train
