# ĐỀ CƯƠNG SƠ BỘ ĐỒ ÁN CUỐI KỲ - HỌC MÁY

## Đề tài
**Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp đặc sản (Cà phê/Lúa) hỗ trợ nông dân**

## Thông tin nhóm
- Nguyễn Hồ Anh Tuấn - 23120185  
- Lê Xuân Trí - 23120099  
- Đàm Tiến Đạt - 23120118  
- Tống Thanh Phúc - 23120158  
- Dương Tuấn Anh - 23120208  

Giảng viên hướng dẫn: Thầy Bùi Tiến Lên  

---

## 1. Giới thiệu & động lực

- Nông nghiệp Việt Nam (lúa, cà phê) bị ảnh hưởng mạnh bởi bệnh lá
- Nông dân khó tiếp cận chuyên gia → chẩn đoán chậm
- Đề tài xây dựng hệ thống AI:
  - Nhận diện bệnh từ ảnh chụp điện thoại
  - Trả kết quả nhanh và nhất quán

### Mục tiêu:
- Thực hiện pipeline ML end-to-end
- Tích hợp thành ứng dụng web
- Phân tích các thách thức:
  - Nhiễu ảnh
  - Mất cân bằng dữ liệu
  - Tương đồng giữa các bệnh

---

## 2. Phát biểu bài toán

- Bài toán: **Multi-class image classification**

### Input:
- Ảnh RGB: `x ∈ R^(H×W×3)`

### Output:
- Nhãn bệnh `y ∈ Y` (healthy + các bệnh)

### Mục tiêu:
- Tối ưu **Macro F1-score**
- Đảm bảo inference nhanh để deploy

### Thách thức:
- Bệnh giống nhau ở giai đoạn sớm
- Biến thiên ánh sáng, góc chụp
- Mất cân bằng dữ liệu
- Ảnh nhiễu, mờ, nhiều lá

---

## 3. Thu thập & chuẩn bị dữ liệu

### 3.1 Nguồn dữ liệu

- Rice Diseases Dataset (~3300 ảnh)
- Rice Leaf Disease Dataset (~19k ảnh sau augmentation)
- Bacterial & Fungal Dataset (~5000 ảnh)
- RoCoLe Coffee Dataset (~1560 ảnh)

### Chuẩn hóa:
- Gom nhãn (taxonomy)
- Tách domain (lúa / cà phê)
- Loại trùng lặp
- Kiểm soát imbalance

-> Dataset cuối: ~10k–15k ảnh

---

### 3.2 Pipeline dữ liệu

1. Hợp nhất metadata
2. Loại ảnh lỗi / trùng
3. Chuẩn hóa nhãn
4. Split:
   - Train 70%
   - Val 15%
   - Test 15%
5. Augmentation sau khi split

---

## 4. Tiền xử lý & EDA

### 4.1 Tiền xử lý

- Resize + normalize
- Chuẩn hóa màu
- Augmentation:
  - Flip, rotation
  - Color jitter
  - Cutout, mixup

---

### 4.2 EDA

- Phân phối lớp
- Visualization mẫu
- Phân tích chất lượng ảnh
- Nhận diện bệnh dễ nhầm

---

## 5. Mô hình

### Các mô hình:

| Model | Vai trò |
|------|--------|
| MobileNetV2 | Baseline nhẹ |
| ResNet50 | CNN mạnh |
| Swin Transformer | Vision transformer |
| DINOv3 | Self-supervised |

### Training:

- Transfer learning
- AdamW + scheduler
- Early stopping (macro F1)

---

## 6. Đánh giá & tuning

### 6.1 Chiến lược

- Fixed train/val/test
- Đánh giá theo:
  - Toàn bộ
  - Theo domain

### Metrics:
- Macro F1 (chính)
- Weighted F1
- Accuracy

### Visualization:
- Confusion matrix
- Learning curve
- ROC

---

### 6.2 Tuning & error analysis

- Baseline:
  - MobileNetV2
  - ResNet50

- Tuning:
  - LR: 1e-5 → 1e-3
  - Batch size: 16–64
  - Dropout: 0–0.5

- Tracking: MLflow

### Error analysis:
- Bệnh giống nhau
- Ảnh mờ
- Nhiều lá
- Healthy vs early disease

---

### 6.3 Quy trình cải thiện

Loop:
1. Train
2. Evaluate
3. Analyze
4. Improve
5. Retrain

---

### 6.4 Chọn model

Dựa trên:
- Macro F1
- Stability
- Inference speed
- Model size
- Calibration

---

## 7. Ứng dụng web

### 7.1 Chức năng

- Upload ảnh
- Trả:
  - Nhãn bệnh
  - Confidence
  - Top-k
  - Gợi ý xử lý

---

### 7.2 Kiến trúc

- Frontend: Next.js + Tailwind
- Backend: FastAPI
- DB: PostgreSQL
- Storage: MinIO
- Cache: Redis

---

### 7.3 Kết quả kỳ vọng

- Model F1 cao
- Web chạy ổn định
- Có demo public

---

## 8. Deployment

### 8.1 Mục tiêu

- Real-time inference
- Public URL
- Scalable system

---

### 8.2 Pipeline

Training → Model → ONNX → API → Web

---

### 8.3 Công nghệ

- Docker
- Kubernetes
- ONNX
- GitHub Actions
- Traefik
- DuckDNS

---

## 9. Kế hoạch & rủi ro

### 9.1 Timeline

| Giai đoạn | Nội dung |
|----------|--------|
| Tuần 3–6 | Data + EDA |
| Tuần 6–10 | Model + tuning |
| Cuối kỳ | Deploy + report |

---

### 9.2 Rủi ro

- Imbalance → weighting
- Domain shift → thêm data
- Quá tải kỹ thuật → ưu tiên core
- Trễ tiến độ → chia milestone

---

### 9.3 Deliverables

- Báo cáo
- Code
- Web app

---