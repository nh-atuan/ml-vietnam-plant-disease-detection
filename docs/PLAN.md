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
| Tuần 7–9 | Training | 3+4 | **Lựa chọn, Huấn luyện, Đánh giá & Tinh chỉnh** – 5 model segmentation trên Kaggle GPU, push HuggingFace Hub, báo cáo tiến độ lần 2 (dự kiến 24/5) |
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

## PHASE 3 — Lựa chọn, Huấn luyện & Đánh giá Mô hình (Segmentation)
> **Tuần 7 → Tuần 9** | **Deadline dự kiến: 24/5**

### Mục tiêu Phase 3
- Mỗi thành viên chọn **1 mô hình segmentation**, tự huấn luyện và đánh giá trên **Kaggle Notebook** (GPU T4/P100, 30h/tuần)
- **Mỗi model được train & evaluate trên 2 notebook riêng biệt** — 1 cho tập lúa (Rice), 1 cho tập cà phê (Coffee) — giúp tách biệt phân phối dữ liệu, dễ debug và chạy song song
- Kết quả evaluation từ cả 5 model sẽ được tổng hợp để **chọn ra best model** cho Phase 4 (tuning)
- Train xong → **push model lên HuggingFace Hub** để nhóm dùng chung qua API
- Commit notebook đã chạy lên repo tại `notebooks/models/<tên_model>/`
- Bài toán: **Instance/Semantic Segmentation** — từ ảnh lá cây xác định vùng bệnh + nhãn bệnh
- Áp dụng Data Augmentation (Affine, Intensity Transformation, CutMix, CutOut, Mixup) để tăng cường dữ liệu và chống overfitting

> **Lý do không dùng MLflow / train local:** PyTorch segmentation models cần GPU; train trên CPU mất hàng chục giờ/epoch. Kaggle cung cấp GPU miễn phí 30h/tuần — đủ để train và tune. MLflow được thay bằng HuggingFace Hub để lưu & serve model.

> **Lý do tách 2 notebook theo dataset:** Lúa và cà phê có đặc điểm hình thái lá, màu sắc và phân phối bệnh khác nhau rõ rệt. Tách notebook giúp mỗi thành viên chạy độc lập trên Kaggle (tránh conflict GPU quota), kết quả per-dataset rõ ràng và dễ so sánh cross-dataset.

### 5 Mô hình Segmentation được chọn

| Model | Đặc điểm | Tham khảo |
|-------|----------|----------|
| **Mask R-CNN** | CNN-based model (Baseline) | [MaskRCNN Resnet50](https://github.com/magnusdtd/AIC-HCMUS-Fragment-Segmentation/blob/main/notebook/gdgoc-hcmus-aic-maskrcnn-resnet50-fpn.ipynb) |
| **YOLO26-seg** | CNN-based model | [Fine-tune YOLO26-seg](https://colab.research.google.com/drive/1tYi19epfw6jUgaIUD03cgsGMC-NXI6KB?usp=sharing) |
| **RF-DETR** | Vision Transformer-based model (SOTA) | [RF-DETR Roboflow Train Guide](https://rfdetr.roboflow.com/learn/train/) |
| **MobileSAM** | Vision Transformer-based model | [MobileSAM Fast Finetuning](https://github.com/KdaiP/MobileSAM-fast-finetuning) |
| **Mask2Former** | Vision Transformer-based model | [Fine-tuning Mask2Former](https://debuggercafe.com/fine-tuning-mask2former/) |

### Phân công công việc

| # | Mô hình | Người phụ trách | Output |
|---|---------|-----------------|--------|
| 3.1 | **Mask R-CNN**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Xuân Trí** | Commit notebook vào `notebooks/models/mask_rcnn/` + push model lên HuggingFace |
| 3.2 | **YOLO26-seg**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Anh Tuấn** | Commit notebook vào `notebooks/models/yolo26_seg/` + push model lên HuggingFace |
| 3.3 | **RF-DETR**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Tống Phúc** | Commit notebook vào `notebooks/models/rf_detr/` + push model lên HuggingFace |
| 3.4 | **MobileSAM**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Đàm Đạt** | Commit notebook vào `notebooks/models/mobilesam/` + push model lên HuggingFace |
| 3.5 | **Mask2Former**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Tuấn Anh** | Commit notebook vào `notebooks/models/mask2former/` + push model lên HuggingFace |
| 3.6 | Tổng hợp kết quả evaluation, lập bảng so sánh đa tiêu chí, **chọn best model** chuyển sang Phase 4, viết báo cáo tiến độ lần 2 phần **Model + Evaluation** | **Cả nhóm** | Bảng so sánh + quyết định best model + Báo cáo tiến độ lần 2 |

### Quy trình mỗi thành viên cần thực hiện

```
[Notebook 1 — Rice dataset]
1. Tạo Kaggle Notebook → kết nối dataset Rice (lọc từ data/processed/ theo plant_type)
2. Implement pipeline: load data → augmentation → train → validate
3. Evaluate: mAP@50, mAP@50:95, mIoU, Dice Score, inference time
4. Lưu best checkpoint Rice → push lên HuggingFace Hub

[Notebook 2 — Coffee dataset]
5. Lặp lại bước 1–4 cho tập cà phê
6. Ghi nhận kết quả cả 2 tập → report vào bảng so sánh nhóm
7. Download notebook đã chạy (có output) → commit vào repo
```

### Thiết lập huấn luyện chung

| Hạng mục | Chi tiết |
|----------|----------|
| **Môi trường** | Kaggle Notebook (GPU T4 x2 hoặc P100) |
| **Dataset** | Upload `data/processed/` lên Kaggle Dataset; lọc theo `plant_type` (rice / coffee) trong notebook |
| **Metrics chính** | mAP@50, mAP@50:95, mIoU, Dice Score |
| **Model hosting** | HuggingFace Hub (public repo của nhóm) |
| **Commit vào repo** | Notebook `.ipynb` đã có output đầy đủ |

### Cấu trúc thư mục

```
notebooks/
  models/
    mask_rcnn/
      train_eval_rice.ipynb       ← Kaggle notebook Rice đã chạy
      train_eval_coffee.ipynb     ← Kaggle notebook Coffee đã chạy
      README.md                   ← mô tả kết quả, link HuggingFace
    yolo26_seg/
      train_eval_rice.ipynb
      train_eval_coffee.ipynb
      README.md
    rf_detr/
    mobilesam/
    mask2former/
```

### Kết quả cần đạt cuối Phase 3

| Hạng mục | Mô tả |
|----------|-------|
| 10 notebooks | Mỗi model 2 notebook Kaggle (Rice + Coffee) đã chạy đầy đủ (train + eval) |
| 10 model checkpoints trên HuggingFace | Best checkpoint per-dataset của mỗi model push lên HF Hub |
| Bảng so sánh | mAP@50, mIoU, inference time, model size — per model, per dataset |
| **Best model được chọn** | 1 model (+ dataset) được chọn để chuyển sang Phase 4 tuning |
| Báo cáo tiến độ 2 | Phần Model + Evaluation hoàn chỉnh |

---

## PHASE 4 — Tinh chỉnh Mô hình Tốt Nhất (Hyperparameter Tuning)
> **Sau khi Phase 3 hoàn thành & best model được chọn**

### Mục tiêu Phase 4
- Chỉ tune **1 model duy nhất** — model được chọn từ bảng so sánh Phase 3
- Sử dụng **RayTune + ASHA (Asynchronous Successive Halving Algorithm)** để tối ưu hyperparameter hiệu quả: early-stop các trial kém ngay từ đầu, tập trung tài nguyên GPU vào các config hứa hẹn
- Kết quả tuning sẽ là checkpoint cuối cùng để export ONNX và deploy

> **Lý do tách tuning ra khỏi Phase 3:** Tuning tất cả 5 model song song là lãng phí GPU quota. Chỉ tune model đã được chứng minh tốt nhất qua evaluation → tối ưu tài nguyên và thời gian.

> **Lý do dùng ASHA thay vì grid/random search:** ASHA tự động loại bỏ sớm các trial kém hiệu năng (early stopping dựa trên intermediate results), cho phép thử nhiều config hơn trong cùng thời gian GPU, đặc biệt phù hợp với giới hạn 30h/tuần của Kaggle.

### Không gian tìm kiếm Hyperparameter (Search Space)

| Hyperparameter | Search Space gợi ý |
|----------------|-------------------|
| **Learning Rate** | `loguniform(1e-5, 1e-2)` |
| **Batch Size** | `choice([4, 8, 16])` |
| **Epochs** | `choice([20, 30, 50])` |
| **Backbone / Neck** | `choice([...])` (tùy model) |
| **Augmentation level** | `choice(['light', 'medium', 'heavy'])` |
| **Weight Decay** | `loguniform(1e-5, 1e-2)` |

### Cấu hình ASHA Scheduler

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

scheduler = ASHAScheduler(
    metric="mAP50",          # metric để đánh giá trial
    mode="max",
    max_t=50,                # số epoch tối đa mỗi trial
    grace_period=5,          # số epoch tối thiểu trước khi có thể prune
    reduction_factor=3,      # mỗi lần halving, giữ lại 1/3 trials tốt nhất
)

tuner = tune.Tuner(
    train_fn,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        scheduler=scheduler,
        num_samples=20,      # tổng số config thử
    ),
)
results = tuner.fit()
```

### Quy trình Phase 4

```
1. Xác nhận best model từ bảng so sánh Phase 3 (cả nhóm quyết định)
2. Tạo Kaggle Notebook mới: tune_<model_name>_<dataset>.ipynb
3. Cài đặt ray[tune] (pip install "ray[tune]")
4. Định nghĩa search space và ASHA scheduler
5. Chạy tuning (num_samples ≥ 15 trials)
6. Lấy best config → train lại với best config trên full train set
7. Evaluate lần cuối trên test set → so sánh với baseline Phase 3
8. Export checkpoint tốt nhất → push lên HuggingFace Hub (override best checkpoint)
9. Commit notebook đã chạy vào repo
```

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 4.1 | Quyết định best model từ bảng so sánh Phase 3 | **Cả nhóm** | Biên bản chọn model (ghi vào README) |
| 4.2 | Setup RayTune + ASHA, implement tuning notebook cho best model | **Người phụ trách model đó** | `notebooks/models/<model>/tune_<dataset>.ipynb` |
| 4.3 | Retrain với best config, evaluate cuối, push checkpoint | **Người phụ trách model đó** | Checkpoint final trên HuggingFace Hub |
| 4.4 | Viết báo cáo phần Tuning: bảng before/after, phân tích lỗi, kết luận | **Người phụ trách model đó** | Phần Tuning trong báo cáo tiến độ 2 |

### Tiêu chí chọn mô hình tốt nhất (từ Phase 3)

1. **mAP@50:95** — độ chính xác segmentation tổng thể
2. **mIoU** — chất lượng phân vùng
3. **Inference time** — phù hợp web serving (mục tiêu < 500ms/ảnh trên CPU)
4. **Model size** — khả năng deploy
5. **Độ ổn định** — train/val gap hợp lý

### Bảng so sánh mô hình Phase 3 (template — điền sau khi train xong)

| Mô hình | Dataset | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) | Size (MB) |
|---------|---------|--------|-----------|------|------|----------------|-----------|
| Mask R-CNN | Rice | — | — | — | — | — | — |
| Mask R-CNN | Coffee | — | — | — | — | — | — |
| YOLO26-seg | Rice | — | — | — | — | — | — |
| YOLO26-seg | Coffee | — | — | — | — | — | — |
| RF-DETR | Rice | — | — | — | — | — | — |
| RF-DETR | Coffee | — | — | — | — | — | — |
| MobileSAM | Rice | — | — | — | — | — | — |
| MobileSAM | Coffee | — | — | — | — | — | — |
| Mask2Former | Rice | — | — | — | — | — | — |
| Mask2Former | Coffee | — | — | — | — | — | — |

### Kết quả cần đạt cuối Phase 4

| Hạng mục | Mô tả |
|----------|-------|
| Best model sau tuning | 1 checkpoint final với hyperparams tối ưu, eval trên test set |
| Bảng before/after tuning | So sánh metrics trước và sau ASHA tuning |
| HuggingFace Hub | Final checkpoint public, dùng được qua HF Inference API |
| Notebook tuning | `tune_<model>_<dataset>.ipynb` đã chạy đầy đủ, có output ray[tune] |
| Báo cáo | Phần Tuning hoàn chỉnh với phân tích lỗi và kết luận chọn model |

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
| 5.4 | **Expert Knowledge Base**: module gợi ý xử lý bệnh theo luật chuyên gia — tra bảng nhãn → hiển thị mô tả bệnh + biện pháp tiếng Việt, hành động cụ thể cho nông dân | **Xuân Trí** | `backend/app/knowledge/`, tích hợp vào API response |
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
- Tích hợp MLOps Dashboard 
- Integration testing end-to-end

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 6.1 | **Docker Compose**: multi-service compose (frontend, backend, PostgreSQL, MinIO, Redis, Traefik), volume mounts, health checks, restart policies | **Tống Phúc** | `deployment/docker-compose.yml` hoàn chỉnh |
| 6.2 | **CI/CD GitHub Actions**: workflow tự động lint, test, build Docker images, push registry, deploy | **Tống Phúc** | `.github/workflows/ci.yml` |
| 6.3 | **DuckDNS + Traefik**: cấu hình tên miền động, HTTPS auto (Let's Encrypt), reverse proxy routing | **Đàm Đạt** | `deployment/traefik/`, URL demo công khai |
| 6.4 | **MLOps Dashboard**: tích hợp MLflow UI vào hệ thống deploy, model versioning & experiment comparison | **Tống Phúc** | MLflow service trong Docker Compose |
| 6.5 | **Integration testing**: end-to-end test pipeline (upload ảnh → predict → verify response), load test cơ bản | **Anh Tuấn** | `tests/`, test scripts |
| 6.6 | **SAM 3 Segmentation**: pseudo-mask generation cho ảnh nhiều lá, tích hợp optional vào API `/segment` | **Đàm Đạt** | `src/segmentation/`, endpoint bổ sung |

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
| S2 | **Mask2Former fine-tune**: Transformer-based universal segmentation SOTA, fine-tune trên dataset lá cây Việt Nam | 3+4 | **Tuấn Anh** | Chiều sâu học thuật, áp dụng mô hình SOTA vào bài toán thực tế |
| S3 | **Expert Knowledge Base** tiếng Việt: gợi ý xử lý bệnh theo luật chuyên gia, hành động cụ thể cho nông dân | 5 | **Xuân Trí** | Giá trị ứng dụng thực tiễn cao, bối cảnh Việt Nam |
| S4 | **Instance Segmentation** thay vì classification: tạo masks thực địa, xác định vùng bệnh + nhãn cùng lúc *(đã xây dựng mask)* | 3+4 | **Tất cả** | Bài toán phong phú hơn, phù hợp ảnh thực địa nhiều lá |
| S5 | **RF-DETR Segmentation**: Detection Transformer của Roboflow, end-to-end fine-tuning | 3+4 | **Anh Tuấn** | Mô hình hiện đại, kết hợp detection + segmentation |
| S6 | **MLOps Dashboard**: tích hợp MLflow UI vào hệ thống deploy, theo dõi model versioning & experiment comparison trực tiếp | 6 | **Tống Phúc** | Quy trình MLOps chuyên nghiệp, dễ mở rộng |

---

## Tổng hợp công việc

| Thành viên | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Phase 7 | Sáng tạo |
|-----------|---------|---------|---------|---------|---------|---------|---------|----------|
| **Lê Xuân Trí** | — | EDA (2.1) | Mask R-CNN: train+eval ×2 datasets (3.1) | Tuning nếu Mask R-CNN là best model (4.2–4.4) | Knowledge Base (5.4) | — | Phần 4–5 báo cáo (7.2) | S3 |
| **Đàm Tiến Đạt** | Dataset (1.1) | — | MobileSAM: train+eval ×2 datasets (3.4) | Tuning nếu MobileSAM là best model (4.2–4.4) | Backend FastAPI (5.2) | DuckDNS/Traefik (6.3) | Phần 1–3 báo cáo (7.1) | S4 |
| **Tống Thanh Phúc** | — | Báo cáo EDA (2.3) | RF-DETR: train+eval ×2 datasets + Báo cáo tiến độ 2 (3.3, 3.6) | Tuning nếu RF-DETR là best model (4.2–4.4) | DB Schema (5.5) | Docker/CI-CD (6.1, 6.2), MLOps (6.4) | Phần 6–7 báo cáo (7.3) | S6 |
| **Dương Tuấn Anh** | Báo cáo P1 (1.2) | — | Mask2Former: train+eval ×2 datasets (3.5) | Tuning nếu Mask2Former là best model (4.2–4.4) | Frontend (5.3) | — | Slide (7.4) | S2 |
| **Nguyễn Hồ Anh Tuấn** | Kiểm duyệt (1.3) | Preprocessing (2.2) | YOLO26-seg: train+eval ×2 datasets (3.2) | Tuning nếu YOLO26-seg là best model (4.2–4.4) | Model Export (5.1) | Integration Test (6.5) | Review & Package (7.5) | S5 |

---

## Checklist skeleton theo output

| Phase | Output chính | Skeleton trong repo |
|---|---|---|
| 3 | Notebooks train+eval (Rice & Coffee) cho 5 model segmentation | `notebooks/models/mask_rcnn/{train_eval_rice,train_eval_coffee}.ipynb`, tương tự cho `yolo26_seg/`, `rf_detr/`, `mobilesam/`, `mask2former/` |
| 3 | Model checkpoints trên HuggingFace Hub (per-dataset) | README trong mỗi folder model ghi link HuggingFace |
| 4 | Notebook tuning best model bằng RayTune ASHA | `notebooks/models/<best_model>/tune_<dataset>.ipynb` |
| 4 | Final model checkpoint sau tuning | Checkpoint final trên HuggingFace Hub |
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
