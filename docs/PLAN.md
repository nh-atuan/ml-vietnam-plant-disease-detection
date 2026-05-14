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

## PHASE 3 — Lựa chọn & Huấn luyện Mô hình (Segmentation)
> **Tuần 7 → Tuần 9** | **Deadline dự kiến: 21/5**

### Mục tiêu Phase 3
- Mỗi thành viên chọn **1 mô hình segmentation**, tự huấn luyện, đánh giá và tinh chỉnh trên **Kaggle Notebook** (GPU T4/P100, 30h/tuần)
- Train xong → **push model lên HuggingFace Hub** để nhóm dùng chung qua API
- Commit notebook đã chạy lên repo tại `notebooks/models/<tên_model>/`
- Bài toán: **Instance/Semantic Segmentation** — từ ảnh lá cây xác định vùng bệnh + nhãn bệnh
- Nên áp dụng Data Augmentation (Affine, Intensity Transformation, CutMix, CutOut, Mixup) để tăng cường dữ liệu và chống overfitting.

> **Lý do không dùng MLflow / train local:** PyTorch segmentation models cần GPU; train trên CPU mất hàng chục giờ/epoch. Kaggle cung cấp GPU miễn phí 30h/tuần — đủ để train và tune. MLflow được thay bằng HuggingFace Hub để lưu & serve model.

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
| 3.1 | **Mask R-CNN**: train + evaluate + tune trên Kaggle | **Xuân Trí** | Commit notebook vào folder `notebooks/models/mask_rcnn/` + push model lên HuggingFace |
| 3.2 | **YOLO26-seg**: train + evaluate + tune trên Kaggle | **Anh Tuấn** | Commit notebook vào folder `notebooks/models/yolo26_seg/` + push model lên HuggingFace |
| 3.3 | **RF-DETR**: train + evaluate + tune trên Kaggle | **Tống Phúc** | Commit notebook vào folder `notebooks/models/rf_detr/` + push model lên HuggingFace |
| 3.4 | **MobileSAM**: train + evaluate + tune trên Kaggle | **Đàm Đạt** | Commit notebook vào folder `notebooks/models/mobilesam/` + push model lên HuggingFace |
| 3.5 | **Mask2Former**: train + evaluate + tune trên Kaggle | **Tuấn Anh** | Commit notebook vào folder `notebooks/models/mask2former/` + push model lên HuggingFace |
| 3.6 | Tổng hợp kết quả, viết bảng so sánh mô hình, chọn model tốt nhất, viết báo cáo tiến độ lần 2 phần **Model + Evaluation** | **Cả nhóm** | Báo cáo tiến độ lần 2 |

### Quy trình mỗi thành viên cần thực hiện

```
1. Tạo Kaggle Notebook → kết nối dataset (upload lên Kaggle Dataset)
2. Implement pipeline: load data → augmentation → train → validate
3. Evaluate: mAP@50, mAP@50:95, mIoU, inference time
4. Hyperparameter tuning: thử ≥ 2 config (LR, batch size, epochs, backbone...)
5. Chọn best checkpoint → export → push lên HuggingFace Hub
6. Download notebook đã chạy (có output) → commit vào repo
```

### Thiết lập huấn luyện chung

| Hạng mục | Chi tiết |
|----------|----------|
| **Môi trường** | Kaggle Notebook (GPU T4 x2 hoặc P100) |
| **Dataset** | Upload `data/processed/` lên Kaggle Dataset, dùng mask đã tạo |
| **Metrics chính** | mAP@50, mAP@50:95, mIoU, Dice Score |
| **Model hosting** | HuggingFace Hub (public repo của nhóm) |
| **Commit vào repo** | Notebook `.ipynb` đã có output đầy đủ |

### Cấu trúc thư mục

```
notebooks/
  models/
    mask_rcnn/
      train_evaluate_tune.ipynb   ← Kaggle notebook đã chạy
      README.md                   ← mô tả kết quả, link HuggingFace
    yolo26_seg/
    rf_detr/
    mobilesam/
    mask2former/
```

### Kết quả cần đạt cuối Phase 3

| Hạng mục | Mô tả |
|----------|-------|
| 5 notebooks | Mỗi model 1 notebook Kaggle đã chạy đầy đủ (train + eval + tune) |
| 5 models trên HuggingFace | Checkpoint tốt nhất của mỗi model được push lên HF Hub |
| Bảng so sánh | mAP@50, mIoU, inference time, model size cho cả 5 model |
| Báo cáo tiến độ 2 | Phần Model + Evaluation hoàn chỉnh |

---

## PHASE 4 — Đánh giá & Tinh chỉnh Mô hình
> *(Đã được tích hợp vào Phase 3 — mỗi thành viên tự train + evaluate + tune trong cùng một Kaggle notebook)*

> **Lý do gộp Phase 3 & 4:** Với workflow trên Kaggle GPU, việc tách riêng training và evaluation/tuning thành hai phase độc lập là không hiệu quả. Mỗi thành viên sẽ thực hiện toàn bộ vòng lặp **train → evaluate → tune** trong cùng một notebook.

### Nội dung evaluation & tuning trong mỗi notebook

| Hạng mục | Yêu cầu |
|----------|----------|
| **Metrics** | mAP@50, mAP@50:95, mIoU, Dice Score, inference time (ms/ảnh) |
| **Visualization** | Hiển thị mask dự đoán vs ground truth trên ≥ 10 ảnh test |
| **Tuning** | Thử ≥ 2 bộ hyperparams (LR, batch size, epochs, augmentation level) |
| **Error analysis** | Nhận xét các trường hợp model dự đoán sai (ảnh khó, bệnh hiếm...) |
| **So sánh** | Bảng trước/sau tuning |

### Tiêu chí chọn mô hình tốt nhất

1. **mAP@50:95** — độ chính xác segmentation tổng thể
2. **mIoU** — chất lượng phân vùng
3. **Inference time** — phù hợp web serving (mục tiêu < 500ms/ảnh trên CPU)
4. **Model size** — khả năng deploy
5. **Độ ổn định** — train/val gap hợp lý

### Bảng so sánh mô hình (template)

| Mô hình | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) | Size (MB) |
|---------|--------|-----------|------|------|----------------|-----------|
| Mask R-CNN | — | — | — | — | — | — |
| YOLO26-seg | — | — | — | — | — | — |
| RF-DETR | — | — | — | — | — | — |
| MobileSAM | — | — | — | — | — | — |
| Mask2Former | — | — | — | — | — | — |

### Kết quả cần đạt

| Hạng mục | Mô tả |
|----------|-------|
| Best model | 1 mô hình được chọn dựa trên bảng so sánh đa tiêu chí |
| HuggingFace Hub | 5 model checkpoints public, dùng được qua HF Inference API |
| Báo cáo tiến độ 2 | Bảng so sánh đầy đủ, phân tích lỗi, chọn model tốt nhất |

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

| Thành viên | Phase 1 | Phase 2 | Phase 3+4 | Phase 5 | Phase 6 | Phase 7 | Sáng tạo |
|-----------|---------|---------|-----------|---------|---------|---------|----------|
| **Lê Xuân Trí** | — | EDA (2.1) | Mask R-CNN: train+eval+tune (3.1) | Knowledge Base (5.4) | — | Phần 4–5 báo cáo (7.2) | S3 |
| **Đàm Tiến Đạt** | Dataset (1.1) | — | MobileSAM: train+eval+tune (3.4) | Backend FastAPI (5.2) | DuckDNS/Traefik (6.3) | Phần 1–3 báo cáo (7.1) | S4 |
| **Tống Thanh Phúc** | — | Báo cáo EDA (2.3) | RF-DETR: train+eval+tune + Báo cáo tiến độ 2 (3.3, 3.6) | DB Schema (5.5) | Docker/CI-CD (6.1, 6.2), MLOps (6.4) | Phần 6–7 báo cáo (7.3) | S6 |
| **Dương Tuấn Anh** | Báo cáo P1 (1.2) | — | Mask2Former: train+eval+tune (3.5) | Frontend (5.3) | — | Slide (7.4) | S2 |
| **Nguyễn Hồ Anh Tuấn** | Kiểm duyệt (1.3) | Preprocessing (2.2) | YOLO26-seg: train+eval+tune (3.2) | Model Export (5.1) | Integration Test (6.5) | Review & Package (7.5) | S5 |

---

## Checklist skeleton theo output

| Phase | Output chính | Skeleton trong repo |
|---|---|---|
| 3+4 | Notebooks train+eval+tune cho 5 model segmentation | `notebooks/models/mask_rcnn/`, `notebooks/models/yolo26_seg/`, `notebooks/models/rf_detr/`, `notebooks/models/mobilesam/`, `notebooks/models/mask2former/` |
| 3+4 | Model checkpoints trên HuggingFace Hub | README trong mỗi folder model ghi link HuggingFace |
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
