# Experiments — DINOv3 Fine-tune (Sáng tạo S2)

**Phụ trách:** Dương Tuấn Anh  
**Phase:** 3 (Training) → 4 (Tuning)

## Mục tiêu
- Khai thác biểu diễn **self-supervised** (DINOv2) để tăng tổng quát hóa
- So sánh **linear probing** vs **full fine-tune**
- Chứng minh lợi thế SSL so với CNN truyền thống (supervised only)

## Cấu trúc thư mục
```
experiments/dinov3/
├── README.md
├── train.py
├── checkpoints/
├── tuning/
└── results/
```

## TODO
- [ ] Phase 3: Linear probing run (freeze backbone, chỉ train head)
- [ ] Phase 3: Full fine-tune run
- [ ] Phase 3: So sánh 2 strategy, log MLflow
- [ ] Phase 4: Hyperparameter tuning
- [ ] Phase 4: Phân tích: DINOv3 có tổng quát hóa tốt hơn trên domain shift?

## Chạy training
```bash
python experiments/dinov3/train.py --config configs/models/dinov3.yaml
```
