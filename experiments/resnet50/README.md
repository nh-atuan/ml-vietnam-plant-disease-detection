# Experiments — ResNet50

**Phụ trách:** Đàm Tiến Đạt  
**Phase:** 3 (Training) → 4 (Tuning)

## Mục tiêu
- Huấn luyện ResNet50 làm **baseline mạnh** (CNN chuẩn chất lượng)
- Transfer learning, thử nghiệm layer-wise LR
- So sánh với MobileNetV2

## Cấu trúc thư mục
```
experiments/resnet50/
├── README.md
├── train.py
├── checkpoints/
├── tuning/
│   ├── search_space.yaml
│   └── best_config.yaml
└── results/
```

## TODO
- [ ] Phase 3: Huấn luyện baseline run
- [ ] Phase 3: Thử layer-wise LR (backbone LR thấp hơn head)
- [ ] Phase 3: Log tất cả runs lên MLflow
- [ ] Phase 4: Hyperparameter tuning (random search → Ray Tune)
- [ ] Phase 4: Ghi nhận best config

## Chạy training
```bash
python experiments/resnet50/train.py --config configs/models/resnet50.yaml
```
