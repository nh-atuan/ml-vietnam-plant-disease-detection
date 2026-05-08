# Experiments — Swin Transformer

**Phụ trách:** Tống Thanh Phúc  
**Phase:** 3 (Training) → 4 (Tuning)

## Mục tiêu
- Huấn luyện Swin Transformer khai thác **attention mechanism**
- So sánh với CNN baselines (MobileNetV2, ResNet50)
- Đánh giá trade-off accuracy vs inference time

## Cấu trúc thư mục
```
experiments/swin_transformer/
├── README.md
├── train.py
├── checkpoints/
├── tuning/
└── results/
```

## TODO
- [ ] Phase 3: Huấn luyện baseline run (swin_t)
- [ ] Phase 3: Log MLflow
- [ ] Phase 4: Tuning hyperparameters
- [ ] Phase 4: So sánh swin_t vs swin_s nếu đủ tài nguyên

## Chạy training
```bash
python experiments/swin_transformer/train.py --config configs/models/swin_transformer.yaml
```
