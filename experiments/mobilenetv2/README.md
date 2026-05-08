# Experiments — MobileNetV2

**Phụ trách:** Lê Xuân Trí  
**Phase:** 3 (Training) → 4 (Tuning)

## Mục tiêu
- Huấn luyện MobileNetV2 làm **baseline nhẹ** (tốc độ suy luận nhanh)
- Transfer learning từ ImageNet pretrained weights
- So sánh chiến lược freeze/unfreeze backbone

## Cấu trúc thư mục
```
experiments/mobilenetv2/
├── README.md           # File này
├── train.py            # Entry point huấn luyện
├── checkpoints/        # Best checkpoints (.pt)
├── tuning/             # Phase 4: hyperparameter tuning results
│   ├── search_space.yaml
│   └── best_config.yaml
└── results/            # Metrics, plots, confusion matrices
```

## TODO
- [ ] Phase 3: Huấn luyện baseline run với config mặc định
- [ ] Phase 3: Thử freeze backbone → unfreeze dần → full fine-tune
- [ ] Phase 3: Log tất cả runs lên MLflow
- [ ] Phase 4: Random search hyperparameters (LR, batch size, weight decay, dropout)
- [ ] Phase 4: Ray Tune nếu kết quả triển vọng
- [ ] Phase 4: Ghi nhận best config YAML

## Chạy training
```bash
python experiments/mobilenetv2/train.py --config configs/models/mobilenetv2.yaml
```
