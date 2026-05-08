# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ
## Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)

---

## Thông tin nhóm

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Lê Xuân Trí | 23120099 |
| 2 | Đàm Tiến Đạt | 23120118 |
| 3 | Tống Thanh Phúc | 23120158 |
| 4 | Dương Tuấn Anh | 23120208 |
| 5 | Nguyễn Hồ Anh Tuấn | 23120185 |

> **Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên

---

## Tổng quan mốc thời gian

| Mốc | Thời điểm | Phase | Nội dung yêu cầu nộp |
|-----|-----------|-------|----------------------|
| Tuần 3 | *(đã qua)* | — | Nộp đề cương (1–2 trang) |
| Tuần 6 | *(đã qua)* | 1–2 | **Data + EDA + Preprocessing** – Dữ liệu sạch, phân tích khám phá, tiền xử lý ảnh |
| Tuần 7–9 | Training | 3 | **Lựa chọn & Huấn luyện** – BaseTrainer, train ≥ 3 models, MLflow tracking |
| Tuần 9–10 | **Báo cáo tiến độ lần 2** | 4 | **Đánh giá & Tinh chỉnh** – Evaluation suite, tuning, error analysis, chọn model tốt nhất |
| Tuần 10–12 | Ứng dụng | 5 | **Xây dựng Ứng dụng** – ONNX export, Backend FastAPI, Frontend Next.js |
| Tuần 12–13 | DevOps | 6 | **Triển khai & DevOps** – Docker Compose, CI/CD, DuckDNS, URL công khai |
| Tuần 13–cuối | Nộp cuối kỳ | 7 | **Báo cáo + Slide + Demo** – Hoàn thiện báo cáo 7 bước, slide bảo vệ, đóng gói |

---

## PHASE 1 — Thu thập & Chuẩn bị Dữ liệu
> **Tuần 3 → Tuần 6** | *(Đã hoàn thành)*

### Mục tiêu Phase 1
- Tìm kiếm, download, cào bằng API hoặc bot & hợp nhất các bộ dataset (Rice, Coffee)
- Chuẩn hóa nhãn, tạo mask, loại ảnh lỗi/trùng lặp
- Kiểm soát imbalance, chia train/val/test
- Thiết lập cấu trúc thư mục project & version control

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 1.1 | Tìm kiếm, download & merge dataset lúa và cà phê | **Đàm Đạt** | `data/raw/` |
| 1.2 | Tổng hợp viết báo cáo tiến độ lần 1 (phần dữ liệu) | **Tuấn Anh** | Phần Thu thập & Chuẩn bị Dữ liệu trong báo cáo |
| 1.3 | Kiểm tra dữ liệu và kiểm duyệt báo cáo tiến độ lần 1 | **Anh Tuấn** | Dữ liệu và báo cáo được kiểm duyệt |

### Kết quả đạt được

| Hạng mục | Mô tả |
|----------|-------|
| Dataset | 7.300 ảnh (lúa: 3.421, cà phê: 3.879), 8 lớp bệnh (`Healthy`, `BrownSpot`, `Hispa`, `LeafBlast`, `LeafMiner`, `PowderyMildew`, `Rust`, `AlgalLeafSpot`), chia 70/15/15 |
| Metadata | `preprocessing_config.json`, `normalization_stats.json` |
| Repo | Cấu trúc thư mục rõ ràng, README có hướng dẫn |
| Tài liệu | Báo cáo tiến độ lần 1 hoàn chỉnh |

---

## PHASE 2 — Tiền xử lý & EDA
> **Tuần 4 → Tuần 6**  | *(Đã hoàn thành)*

### Mục tiêu Phase 2
- Tiền xử lý ảnh: resize, normalize, chuẩn hóa màu (canvas 256×256, padding giữ tỉ lệ)
- Xây dựng pipeline augmentation (RandomResizedCrop, Flip, ColorJitter, MixUp, CutMix,...)
- Phân tích khám phá dữ liệu (EDA) toàn diện: phân phối lớp, kích thước ảnh, độ sáng, cặp bệnh dễ nhầm

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 2.1 | EDA: phân phối lớp, thống kê, visualization, nhận diện cặp bệnh dễ nhầm | **Xuân Trí** | Notebook EDA + biểu đồ |
| 2.2 | Pipeline tiền xử lý & augmentation (chuẩn hóa nhãn, chia split, resize, normalize...) | **Anh Tuấn** | Notebook Preprocessing, `data/processed/`, `data/splits/` |
| 2.3 | Tổng hợp insight, viết báo cáo phần Tiền xử lý & EDA | **Tống Phúc** | Phần EDA trong báo cáo tiến độ lần 1 |

### Kết quả đạt được

| Hạng mục | Mô tả |
|----------|-------|
| Notebook EDA | Biểu đồ phân phối, Bhattacharyya distance, confusion pairs |
| Script tiền xử lý | Pipeline đầy đủ từ raw → processed (7.149 ảnh sạch) |
| Insight | Cặp dễ nhầm: BrownSpot↔LeafBlast, AlgalLeafSpot↔Rust |
| Augmentation | MixUp (α=0.4), CutMix (α=1.0), WeightedRandomSampler |

---

## PHASE 3 — Lựa chọn & Huấn luyện Mô hình
> **Tuần 7 → Tuần 9** | **Deadline dự kiến: 12/5**

### Mục tiêu Phase 3
- Xây dựng BaseTrainer và hạ tầng huấn luyện chung (training loop, MLflow tracking)
- Huấn luyện ≥ 3 mô hình theo yêu cầu môn học (MobileNetV2, ResNet50, Swin Transformer)
- Thử nghiệm thêm DINOv3 fine-tune (sáng tạo)
- Thiết kế config system chuẩn hóa cho toàn bộ thực nghiệm

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 3.1 | Xây dựng `BaseTrainer`: training loop, early stopping, LR scheduler (CosineAnnealing / ReduceLROnPlateau), checkpoint theo macro F1 val, mixed precision (AMP), tích hợp MLflow logging | **Anh Tuấn** | `src/training/trainer.py`, `src/training/callbacks.py` |
| 3.2 | Refactor `ModelFactory`: registry pattern cho tất cả kiến trúc, chuẩn hóa interface `create_model(name, num_classes, pretrained)` | **Anh Tuấn** | `src/models/model_factory.py` |
| 3.3 | Thiết kế config system: YAML config riêng cho mỗi model + shared training defaults | **Anh Tuấn** | `configs/training_defaults.yaml`, `configs/models/*.yaml` |
| 3.4 | Huấn luyện **MobileNetV2** (baseline nhẹ): transfer learning từ ImageNet, freeze backbone → unfreeze dần, log toàn bộ lên MLflow | **Xuân Trí** | `experiments/mobilenetv2/`, checkpoint `.pt` |
| 3.5 | Huấn luyện **ResNet50** (baseline mạnh): transfer learning, thử nghiệm layer-wise LR, so sánh với MobileNetV2 | **Đàm Đạt** | `experiments/resnet50/`, checkpoint `.pt` |
| 3.6 | Huấn luyện **Swin Transformer**: khai thác attention mechanism, thử nghiệm patch size, log MLflow | **Tống Phúc** | `experiments/swin_transformer/`, checkpoint `.pt` |
| 3.7 | Huấn luyện **DINOv3 fine-tune** *(sáng tạo)*: self-supervised pre-training → linear probing vs full fine-tune, so sánh tổng quát hóa | **Tuấn Anh** | `experiments/dinov3/`, checkpoint `.pt` |

### Chi tiết kỹ thuật Phase 3

**Thiết lập huấn luyện chung:**
- Framework: PyTorch + torchvision
- Optimizer: AdamW + CosineAnnealingLR (hoặc ReduceLROnPlateau)
- Early stopping theo macro F1 validation (patience = 5–10 epochs)
- Mixed precision (AMP) để tăng tốc huấn luyện
- Tracking: MLflow (params, metrics theo epoch, artifacts: confusion matrix, checkpoint)

**Không gian siêu tham số ban đầu:**

| Siêu tham số | Khoảng tìm kiếm |
|---|---|
| Learning rate | 1e-5 → 1e-3 (log scale) |
| Batch size | {16, 32, 64} |
| Weight decay | 1e-5 → 1e-2 |
| Dropout | 0.0 → 0.5 |
| Mức augmentation | yếu / trung bình / mạnh |

### Kết quả cần đạt cuối Phase 3

| Hạng mục | Mô tả |
|----------|-------|
| BaseTrainer | Training loop hoàn chỉnh, tái sử dụng cho tất cả model |
| Checkpoints | ≥ 3 mô hình đã train với cấu hình chuẩn (baseline run) |
| MLflow | Tất cả runs được log, có thể compare trong UI |
| Config system | YAML config cho mỗi model, shared defaults |

---

## PHASE 4 — Đánh giá & Tinh chỉnh Mô hình
> **Tuần 9 → Tuần 10** | **Deadline dự kiến: 15/5**

### Mục tiêu Phase 4
- Xây dựng evaluation suite chuẩn hóa (confusion matrix, F1, ROC, inference benchmark)
- Hyperparameter tuning 2 pha (random search → Ray Tune)
- Error analysis theo 4 nhóm lỗi
- Robustness evaluation với nhiễu tổng hợp (sáng tạo)
- Chọn mô hình tốt nhất theo tiêu chí đa mục tiêu
- Viết Báo cáo tiến độ lần 2

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 4.1 | Xây dựng `Evaluator`: confusion matrix (đếm + chuẩn hóa), macro/weighted F1 theo lớp & theo domain (rice/coffee), ROC one-vs-rest, inference time benchmark (ms/ảnh) | **Anh Tuấn** | `src/evaluation/evaluator.py`, `src/evaluation/metrics.py` |
| 4.2 | Hyperparameter tuning **MobileNetV2**: Pha 1 random search → Pha 2 Ray Tune cho config triển vọng, log MLflow | **Xuân Trí** | `experiments/mobilenetv2/tuning/`, best config YAML |
| 4.3 | Hyperparameter tuning **ResNet50**: tương tự 2 pha, so sánh trước/sau tuning | **Đàm Đạt** | `experiments/resnet50/tuning/`, best config YAML |
| 4.4 | Hyperparameter tuning **Swin Transformer**: tương tự 2 pha | **Tống Phúc** | `experiments/swin_transformer/tuning/`, best config YAML |
| 4.5 | Hyperparameter tuning **DINOv3**: tương tự 2 pha | **Tuấn Anh** | `experiments/dinov3/tuning/`, best config YAML |
| 4.6 | **Error analysis**: top-K dự đoán sai confidence cao, phân nhóm (1-visual similarity, 2-ảnh mờ/thiếu sáng, 3-bố cục phức tạp, 4-healthy vs early disease) | **Xuân Trí** | `notebooks/phase4_error_analysis_tri.ipynb`, báo cáo lỗi |
| 4.7 | **Robustness evaluation** *(sáng tạo)*: tạo test set nhiễu tổng hợp (blur, brightness shift, contrast change), đo drop F1 theo mức nhiễu | **Anh Tuấn** | `src/evaluation/robustness.py`, notebook kết quả |
| 4.8 | Tổng hợp bảng so sánh mô hình, chọn mô hình tốt nhất (tiêu chí đa mục tiêu), viết phần **Model + Evaluation** cho Báo cáo tiến độ lần 2 | **Tống Phúc** | Báo cáo tiến độ lần 2 |

### Chiến lược tuning (2 pha)
- **Pha 1 (thăm dò):** random search ~10–20 trial trong không gian hẹp
- **Pha 2 (tinh chỉnh):** Ray Tune với ASHA scheduler cho mô hình triển vọng

### Tiêu chí chọn mô hình cuối cùng (theo proposal §6.4)
1. **Hiệu năng dự đoán:** Macro F1 cao và ổn định trên test set
2. **Độ ổn định học:** khoảng cách train–val hợp lý, không overfit
3. **Chi phí suy luận:** inference time phù hợp web serving
4. **Tính triển khai:** kích thước model, khả năng export ONNX
5. **Độ tin cậy:** confidence được hiệu chỉnh tốt (calibration)

### Bảng so sánh mô hình (template)

| Mô hình | Macro F1 | Weighted F1 | Accuracy | Inference (ms/img) | Size (MB) |
|---------|----------|-------------|----------|--------------------|-----------| 
| MobileNetV2 | — | — | — | — | — |
| ResNet50 | — | — | — | — | — |
| Swin Transformer | — | — | — | — | — |
| DINOv3 fine-tune | — | — | — | — | — |

### Kết quả cần đạt cuối Phase 4

| Hạng mục | Mô tả |
|----------|-------|
| Evaluation suite | Evaluator chạy được cho tất cả model, output chuẩn hóa |
| Best checkpoints | Mỗi model có best checkpoint sau tuning |
| Bảng so sánh | Đầy đủ 5 metrics, phân tích theo domain |
| Error Analysis | Báo cáo 4 nhóm lỗi, top-K sai confidence cao |
| Robustness | Báo cáo drop F1 theo 3 loại nhiễu |
| Báo cáo tiến độ 2 | Phần Model + Evaluation đầy đủ, có biểu đồ và bảng |

---

## PHASE 5 — Xây dựng Ứng dụng
> **Tuần 10 → Tuần 12** | **Deadline: Sau Báo cáo tiến độ lần 2**

### Mục tiêu Phase 5
- Export mô hình tốt nhất sang ONNX, đăng ký MLflow Model Registry
- Xây dựng Backend FastAPI với inference endpoint
- Xây dựng Frontend Next.js + Tailwind CSS
- Thiết kế database schema và API specification
- Tích hợp Expert Knowledge Base tiếng Việt

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 5.1 | **Model Export & Registry**: export sang ONNX, benchmark inference ONNX vs PyTorch, đăng ký MLflow Model Registry, viết script tự động export | **Anh Tuấn** | `models/best_model.onnx`, `scripts/export_onnx.py`, MLflow Registry entry |
| 5.2 | **Backend FastAPI**: REST API `/predict` (nhận ảnh → trả nhãn + top-k + confidence), kết nối PostgreSQL (log dự đoán), MinIO (lưu ảnh gốc), Redis (cache kết quả TTL 1h), Swagger docs | **Đàm Đạt** | `backend/app/`, Docker service backend |
| 5.3 | **Frontend Next.js**: trang upload ảnh, hiển thị kết quả chẩn đoán (nhãn, confidence, top-k, gợi ý xử lý), giao diện mobile-first responsive | **Tuấn Anh** | `frontend/`, UI demo hoạt động |
| 5.4 | **Expert Knowledge Base** *(sáng tạo)*: module gợi ý xử lý bệnh theo luật chuyên gia — tra bảng nhãn → hiển thị mô tả bệnh + biện pháp tiếng Việt, hành động cụ thể cho nông dân | **Xuân Trí** | `backend/app/knowledge/`, tích hợp vào API response |
| 5.5 | **Database schema & API docs**: thiết kế PostgreSQL schema (predictions, images, users), viết OpenAPI spec, review API contracts giữa frontend–backend | **Tống Phúc** | Schema SQL, API specification |

### Kiến trúc hệ thống

```
User
 └─→ Frontend (Next.js + Tailwind)
        └─→ POST /predict → Backend (FastAPI)
                              ├── MinIO      ← lưu ảnh gốc
                              ├── Redis      ← cache kết quả (TTL 1h)
                              ├── ONNX Runtime ← inference model
                              ├── Knowledge Base ← gợi ý xử lý bệnh
                              └── PostgreSQL ← log dự đoán
```

### Kết quả cần đạt cuối Phase 5

| Hạng mục | Mô tả |
|----------|-------|
| ONNX Model | Export thành công, inference < 500ms/ảnh trên CPU |
| Backend API | FastAPI ổn định, `/predict` trả kết quả đúng, có Swagger docs |
| Frontend | Giao diện đẹp, responsive, demo được trên điện thoại |
| Knowledge Base | Hiển thị gợi ý xử lý phù hợp cho từng loại bệnh (tiếng Việt) |
| DB Schema | PostgreSQL schema hoàn chỉnh, migration scripts |

---

## PHASE 6 — Triển khai & DevOps
> **Tuần 12 → Tuần 13** | **Deadline: Sau Báo cáo tiến độ lần 2**

### Mục tiêu Phase 6
- Containerize toàn bộ hệ thống bằng Docker Compose
- Thiết lập CI/CD với GitHub Actions
- Deploy lên cloud có URL công khai (DuckDNS + Traefik)
- Tích hợp MLOps Dashboard (sáng tạo)
- Integration testing end-to-end

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 6.1 | **Docker Compose**: multi-service compose (frontend, backend, PostgreSQL, MinIO, Redis, Traefik), volume mounts, health checks, restart policies | **Tống Phúc** | `deployment/docker-compose.yml` hoàn chỉnh |
| 6.2 | **CI/CD GitHub Actions**: workflow tự động lint, test, build Docker images, push registry, deploy | **Tống Phúc** | `.github/workflows/ci.yml` |
| 6.3 | **DuckDNS + Traefik**: cấu hình tên miền động, HTTPS auto (Let's Encrypt), reverse proxy routing | **Đàm Đạt** | `deployment/traefik/`, URL demo công khai |
| 6.4 | **MLOps Dashboard** *(sáng tạo)*: tích hợp MLflow UI vào hệ thống deploy, model versioning & experiment comparison | **Tống Phúc** | MLflow service trong Docker Compose |
| 6.5 | **Integration testing**: end-to-end test pipeline (upload ảnh → predict → verify response), load test cơ bản | **Anh Tuấn** | `tests/`, test scripts |
| 6.6 | **SAM 3 Segmentation** *(sáng tạo)*: pseudo-mask generation cho ảnh nhiều lá, tích hợp optional vào API `/segment` | **Đàm Đạt** | `src/segmentation/`, endpoint bổ sung |

### Stack triển khai

| Thành phần | Vai trò |
|---|---|
| Docker | Containerize toàn bộ services |
| Kubernetes | Tuỳ chọn mở rộng theo proposal nếu nhóm có đủ thời gian/hạ tầng; Docker Compose vẫn là baseline demo |
| Traefik | Reverse proxy, routing, HTTPS |
| DuckDNS | Tên miền động cho URL demo công khai |
| GitHub Actions | CI/CD tự động build & deploy |
| ONNX Runtime | Inference tối ưu tốc độ |
| MLflow Model Registry | Quản lý phiên bản mô hình |

### Kết quả cần đạt cuối Phase 6

| Hạng mục | Mô tả |
|----------|-------|
| Docker Compose | `docker compose up` → toàn bộ hệ thống hoạt động |
| CI/CD | Push code → auto build & deploy |
| URL công khai | Demo truy cập được từ internet qua DuckDNS |
| MLOps | MLflow UI accessible, model versions tracked |
| Tests | E2E test pass, basic load test report |

---

## PHASE 7 — Hoàn thiện Báo cáo, Slide & Demo
> **Tuần 13 → Tuần cuối** | **Deadline: Sau Báo cáo tiến độ lần 2**

### Mục tiêu Phase 7
- Hoàn thiện báo cáo khoa học đầy đủ 7 bước quy trình theo yêu cầu môn học
- Chuẩn bị slide bảo vệ súc tích, trực quan
- Review code, viết README đầy đủ, đóng gói nộp bài

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 7.1 | Viết **phần 1–3 báo cáo cuối**: Giới thiệu, Phát biểu bài toán, Thu thập & Chuẩn bị dữ liệu | **Đàm Đạt** | Phần 1–3 báo cáo (PDF) |
| 7.2 | Viết **phần 4–5 báo cáo cuối**: Tiền xử lý & EDA, Lựa chọn & Huấn luyện Mô hình | **Xuân Trí** | Phần 4–5 báo cáo (PDF) |
| 7.3 | Viết **phần 6–7 + Kết luận**: Đánh giá & Tuning, Xây dựng Ứng dụng & Triển khai | **Tống Phúc** | Phần 6–7 + Kết luận (PDF) |
| 7.4 | Thiết kế **Slide bảo vệ**: tóm tắt 7 bước, bảng so sánh mô hình, demo ảnh, kiến trúc hệ thống, điểm sáng tạo | **Tuấn Anh** | Slide PDF/PPTX (10–15 trang) |
| 7.5 | **Review & packaging**: kiểm tra code sạch, comment, docstring; README đầy đủ; đóng gói ZIP nộp bài; đảm bảo repo public | **Anh Tuấn** | ZIP nộp bài, README hoàn chỉnh |

### Minh chứng nộp cuối kỳ

| Minh chứng | Mô tả |
|-----------|-------|
| Báo cáo (PDF) | Đầy đủ 7 bước, có bảng, biểu đồ, phân tích sâu |
| Mã nguồn (ZIP) | Code sạch, comment, chạy lại được |
| Mô hình (`.onnx`/`.pt`) | Checkpoint tốt nhất, kèm hướng dẫn load |
| Slide (PDF/PPTX) | Súc tích, trực quan, sẵn sàng bảo vệ |
| Link ứng dụng (URL) | Demo truy cập công khai qua DuckDNS |

---

## Đề xuất Điểm Sáng Tạo (10%)

> Mục tiêu: tạo ra sản phẩm đột phá, vượt ra ngoài yêu cầu tối thiểu, có giá trị thực tiễn cao.

| # | Ý tưởng sáng tạo | Phase | Người phụ trách | Giá trị mang lại |
|---|-----------------|-------|-----------------|-----------------| 
| S1 | **Human-in-the-loop Labeling Tool** (Streamlit): AI pre-label bằng Gemma 4 + kiểm duyệt thủ công, điều hướng bàn phím, phát hiện trùng MD5 *(đã hoàn thành)* | 1–2 | Tất cả | Pipeline thu thập dữ liệu tiếng Việt độc đáo, tái sử dụng được |
| S2 | **DINOv3 Fine-tune**: self-supervised pre-training cải thiện tổng quát hóa, so sánh với CNN truyền thống | 3 | **Tuấn Anh** | Chiều sâu học thuật, chứng minh lợi thế SSL |
| S3 | **Expert Knowledge Base** tiếng Việt: gợi ý xử lý bệnh theo luật chuyên gia, hành động cụ thể cho nông dân | 5 | **Xuân Trí** | Giá trị ứng dụng thực tiễn cao, bối cảnh Việt Nam |
| S4 | **Segmentation với SAM 3**: mở rộng sang classification + segmentation, pseudo-mask → refine thủ công *(đã xây dựng cơ sở)* | 6 | **Đàm Đạt** | Bài toán phong phú hơn, phù hợp ảnh thực địa nhiều lá |
| S5 | **Robustness Evaluation**: đánh giá độ bền trước nhiễu thực địa (blur, brightness shift, contrast change) bằng test set nhiễu tổng hợp | 4 | **Anh Tuấn** | Phân tích chuyên sâu, tăng tin cậy khi deploy thực tế |
| S6 | **MLOps Dashboard**: tích hợp MLflow UI vào hệ thống deploy, theo dõi model versioning & experiment comparison trực tiếp | 6 | **Tống Phúc** | Quy trình MLOps chuyên nghiệp, dễ mở rộng |

---

## Tổng hợp công việc

| Thành viên | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Phase 7 | Sáng tạo |
|-----------|---------|---------|---------|---------|---------|---------|---------|----------|
| **Lê Xuân Trí** | — | EDA (2.1) | MobileNetV2 (3.4) | Tuning MNV2 (4.2), Error Analysis (4.6) | Knowledge Base (5.4) | — | Phần 4–5 báo cáo (7.2) | S3 |
| **Đàm Tiến Đạt** | Dataset (1.1) | — | ResNet50 (3.5) | Tuning RN50 (4.3) | Backend FastAPI (5.2) | DuckDNS/Traefik (6.3), SAM3 (6.6) | Phần 1–3 báo cáo (7.1) | S4 |
| **Tống Thanh Phúc** | — | Báo cáo EDA (2.3) | Swin Transformer (3.6) | Tuning SwinT (4.4), Báo cáo M2 (4.8) | DB Schema (5.5) | Docker/CI-CD (6.1, 6.2), MLOps (6.4) | Phần 6–7 báo cáo (7.3) | S6 |
| **Dương Tuấn Anh** | Báo cáo P1 (1.2) | — | DINOv3 (3.7) | Tuning DINOv3 (4.5) | Frontend (5.3) | — | Slide (7.4) | S2 |
| **Nguyễn Hồ Anh Tuấn** | Kiểm duyệt (1.3) | Preprocessing (2.2) | Trainer + Config (3.1–3.3) | Evaluator + Robustness (4.1, 4.7) | Model Export (5.1) | Integration Test (6.5) | Review & Package (7.5) | S5 |

---

## Checklist skeleton theo output

| Phase | Output chính | Skeleton trong repo |
|---|---|---|
| 3 | Trainer, callbacks, model factory, config từng model | `src/training/`, `src/models/model_factory.py`, `configs/training_defaults.yaml`, `configs/models/*.yaml` |
| 3 | Thư mục experiment cho 4 mô hình | `experiments/mobilenetv2/`, `experiments/resnet50/`, `experiments/swin_transformer/`, `experiments/dinov3/` |
| 4 | Evaluation suite, robustness, error analysis, tuning | `src/evaluation/`, `notebooks/phase4_error_analysis_tri.ipynb`, `notebooks/phase4_robustness_evaluation_anh_tuan.ipynb`, `experiments/*/tuning/` |
| 5 | ONNX export, model metadata | `scripts/export_onnx.py`, `models/README.md`, `models/class_names.json` |
| 5 | Backend, knowledge base, DB schema, API contract | `backend/app/`, `backend/app/knowledge/`, `backend/app/db/schema.sql`, `docs/api-spec.md` |
| 5 | Frontend Next.js skeleton | `frontend/package.json`, `frontend/src/app/`, `frontend/Dockerfile` |
| 6 | Docker Compose, CI/CD, Traefik, MLflow, tests, SAM 3 | `deployment/docker-compose.yml`, `.github/workflows/ci.yml`, `deployment/traefik/`, `tests/`, `src/segmentation/` |

---

## Quy ước làm việc nhóm

- **Git workflow:** feature branch theo task → PR → review trước khi merge vào `main`
- **Họp nhóm:** ít nhất 1 lần/tuần để sync tiến độ, báo sớm blocker
- **Môi trường:** dùng chung `requirements.txt`, tạo virtual env riêng
- **Naming:** `notebooks/<phase>_<topic>_<author>.ipynb`; script đặt tên theo chức năng trong `src/`
- **Tracking:** cập nhật trạng thái task trong file này hoặc GitHub Issues
