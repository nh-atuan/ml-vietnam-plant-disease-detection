# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ
## Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)

---

## Thông tin nhóm

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Nguyễn Hồ Anh Tuấn | 23120185 |
| 2 | Lê Xuân Trí | 23120099 |
| 3 | Đàm Tiến Đạt | 23120118 |
| 4 | Tổng Thanh Phúc | 23120158 |
| 5 |Dương Tuấn Anh | 23120208 |

> **Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên

---

## Tổng quan mốc thời gian

| Mốc | Thời điểm | Nội dung yêu cầu nộp |
|-----|-----------|----------------------|
| 🔵 Tuần 3 | *(đã qua)* | Nộp đề cương (1–2 trang) |
| 🟡 Tuần 6 | Báo cáo tiến độ lần 1 | **Data + EDA** – Dữ liệu sạch, phân tích khám phá |
| 🟠 Tuần 10 | Báo cáo tiến độ lần 2 | **Model + Evaluation** – Mô hình đã huấn luyện, đánh giá |
| 🔴 Tuần cuối | Nộp cuối kỳ | **Deploy + Báo cáo + Slide + Demo** |

---

## PHASE 1 — Thu thập & Chuẩn bị Dữ liệu
> 📅 **Tuần 3 → Tuần 6** | 🎯 Deadline nộp: **Tuần 6 (Báo cáo tiến độ lần 1)**

### Mục tiêu Phase 1
- Tìm kiếm, download, cào bằng API hoặc bot & hợp nhất các bộ dataset (Rice, Coffee)
- Chuẩn hóa nhãn (nếu có), tạo mask, loại ảnh lỗi/trùng lặp
- Kiểm soát imbalance, chia train/val/test
- Thiết lập cấu trúc thư mục project & version control

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 1.1 | Tìm kiếm, download & merge dataset lúa và cà phê | **Đàm Đạt** | `data/raw/` |
| 1.2 | Tổng hợp viết báo cáo tiến độ lần 1 (dựa trên phần dữ liệu) | **Tuấn Anh** | Phần Thu thập & Chuẩn bị Dữ liệu trong Báo cáo tiến độ lần 1 |
| 1.3 | Kiểm tra dữ liệu và báo cáo tiến độ lần 1 | **Anh Tuấn** | Dữ liệu và báo cáo được kiểm duyệt |

### Kết quả cần đạt cuối Phase 1

| Hạng mục | Mô tả |
|----------|-------|
| Dataset | ~10k–15k ảnh sạch, đã gán nhãn, đã chia split |
| Metadata | File CSV chứa đường dẫn, nhãn, nguồn gốc |
| Repo | Cấu trúc thư mục rõ ràng, README có hướng dẫn |
| Tài liệu báo cáo | Tổng số mẫu, phân phối nhãn, mô tả nguồn |

---

## PHASE 2 — Tiền xử lý & EDA
> 📅 **Tuần 4 → Tuần 6** *(song song với Phase 1)* | 🎯 Deadline nộp: **Tuần 6 (Báo cáo tiến độ lần 1)**

### Mục tiêu Phase 2
- Tiền xử lý ảnh: resize, normalize, chuẩn hóa màu
- Xây dựng pipeline augmentation
- Phân tích khám phá dữ liệu (EDA) toàn diện

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 2.1 | Khám phá dữ liệu (EDA): Phân phối lớp, thống kê, visualization, nhận diện bệnh dễ nhầm | **Xuân Trí** | Notebook EDA + biểu đồ, hình ảnh |
| 2.2 | Pipeline tiền xử lý ảnh và augmentation (chuẩn hóa nhãn, chia split, resize, normalize, Flip, v.v) | **Anh Tuấn** | Notebook Preprocessing, `data/processed/`, `data/splits/` |
| 2.3 | Tổng hợp insight, viết báo cáo phần Tiền xử lý & EDA (cho Báo cáo tiến độ lần 1) | **Tổng Phúc** | Phần Tiền xử lý & EDA trong Báo cáo tiến độ lần 1|

### Kết quả cần đạt cuối Phase 2

| Hạng mục | Mô tả |
|----------|-------|
| Notebook EDA | Đầy đủ biểu đồ phân phối, visualizations |
| Script tiền xử lý | Có thể chạy pipeline đầy đủ từ raw → ready |
| Insight | Nêu được đặc điểm dữ liệu, bệnh dễ nhầm |
| Tài liệu báo cáo  | Phần Data + EDA cho báo cáo Báo cáo tiến độ lần 1 |

---

## PHASE 3 — Xây dựng & Huấn luyện Mô hình
> 📅 **Tuần 6 → Tuần 10** | 🎯 Deadline nộp: **Tuần 10 (Báo cáo tiến độ lần 2)**

### Mục tiêu Phase 3
- Implement ≥ 3 mô hình (theo yêu cầu đề bài)
- Huấn luyện với transfer learning
- Theo dõi thí nghiệm bằng MLflow

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 3.1 | Implement & train **MobileNetV2** (baseline nhẹ, transfer learning) | **Xuân Trí** | Model checkpoint, kết quả train |
| 3.2 | Implement & train **ResNet50** (CNN mạnh, transfer learning) | **Đàm Đạt** | Model checkpoint, kết quả train |
| 3.3 | Implement & train **Swin Transformer** (Vision Transformer) | **Anh Tuấn** | Model checkpoint, kết quả train |
| 3.4 | Implement & train **DINOv2** (Self-supervised, backbone mạnh) | **Tuấn Anh** | Model checkpoint, kết quả train |
| 3.5 | Thiết lập MLflow tracking, chuẩn hóa logging metric, quản lý experiment | **Tổng Phúc** | MLflow server/logs, script training chuẩn |

### Kết quả cần đạt cuối Phase 3

| Hạng mục | Mô tả |
|----------|-------|
| ≥ 3 models | Đã train xong, có checkpoint lưu |
| Metrics | Macro F1, Weighted F1, Accuracy trên val set |
| MLflow | Đã log đầy đủ các thí nghiệm |
| So sánh | Bảng so sánh hiệu năng các model |

---

## PHASE 4 — Đánh giá, Tuning & Phân tích Lỗi
> 📅 **Tuần 8 → Tuần 10** *(song song với Phase 3)* | 🎯 Deadline nộp: **Tuần 10 (Báo cáo tiến độ lần 2)**

### Mục tiêu Phase 4
- Đánh giá toàn diện trên test set
- Tuning hyperparameters
- Phân tích lỗi, chọn model tốt nhất

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 4.1 | Đánh giá model trên test set: Confusion matrix, Learning curve, ROC | **Anh Tuấn** | Notebook đánh giá, biểu đồ |
| 4.2 | Tuning hyperparameters (LR: 1e-5→1e-3, Batch size: 16–64, Dropout: 0–0.5) | **Xuân Trí** | Script tuning, kết quả tuning |
| 4.3 | Error analysis: bệnh nhầm, ảnh mờ, nhiều lá, healthy vs early disease | **Đàm Đạt** | Notebook phân tích lỗi |
| 4.4 | Đánh giá theo domain (lúa / cà phê), kiểm tra domain shift | **Tổng Phúc** | Báo cáo domain evaluation |
| 4.5 | Chọn model cuối (dựa trên F1, stability, inference speed, size), export ONNX | **Tuấn Anh** | Model ONNX + benchmark |

### Kết quả cần đạt cuối Phase 4

| Hạng mục | Mô tả |
|----------|-------|
| Model tốt nhất | Đã chọn, đã export (h5/pt/pkl/onnx) |
| Đánh giá | Confusion matrix, ROC, metrics đầy đủ |
| Error analysis | Hiểu rõ điểm yếu, đã cải thiện |
| Tài liệu | Phần Model + Evaluation cho báo cáo Báo cáo tiến độ lần 2 |

---

## PHASE 5 — Xây dựng Ứng dụng Web
> 📅 **Tuần 10 → Tuần cuối** | 🎯 Deadline nộp: **Tuần cuối (Nộp cuối kỳ)**

### Mục tiêu Phase 5
- Xây dựng Backend API phục vụ inference
- Xây dựng Frontend giao diện người dùng
- Tích hợp Database và Storage

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 5.1 | Backend API với **FastAPI**: endpoint upload ảnh, predict, trả kết quả + top-k + gợi ý | **Anh Tuấn** | `backend/` – API chạy được |
| 5.2 | Frontend với **Next.js + Tailwind**: UI upload ảnh, hiển thị kết quả, confidence | **Xuân Trí** | `frontend/` – giao diện hoàn chỉnh |
| 5.3 | Tích hợp Database (PostgreSQL) lưu lịch sử dự đoán + Storage (MinIO) lưu ảnh | **Đàm Đạt** | Schema DB, storage hoạt động |
| 5.4 | Cache (Redis) cho model inference, tối ưu response time | **Tổng Phúc** | Redis integrated, benchmark |
| 5.5 | Tích hợp model ONNX vào backend, test end-to-end toàn bộ pipeline | **Tuấn Anh** | Pipeline hoàn chỉnh, test pass |

### Kết quả cần đạt cuối Phase 5

| Hạng mục | Mô tả |
|----------|-------|
| Backend | FastAPI chạy ổn định, predict trả kết quả đúng |
| Frontend | Giao diện thân thiện, hiển thị đầy đủ kết quả |
| Integration | DB, Storage, Cache tích hợp thành công |
| End-to-end | Upload ảnh → Kết quả chẩn đoán hoạt động |

---

## PHASE 6 — Triển khai & Demo
> 📅 **Tuần 12 → Tuần cuối** | 🎯 Deadline nộp: **Tuần cuối (Nộp cuối kỳ)**

### Mục tiêu Phase 6
- Containerize toàn bộ hệ thống
- Deploy lên cloud, có Public URL
- Demo sản phẩm

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 6.1 | Viết **Dockerfile** và **docker-compose** cho toàn bộ service (backend, frontend, db, redis, minio) | **Anh Tuấn** | `docker-compose.yml` hoạt động |
| 6.2 | Thiết lập **GitHub Actions** CI/CD (test → build → deploy tự động) | **Xuân Trí** | Pipeline CI/CD |
| 6.3 | Deploy lên cloud server, cấu hình **Traefik + DuckDNS** có HTTPS | **Đàm Đạt** | Public URL hoạt động |
| 6.4 | Stress test hệ thống sau deploy, fix bug, tối ưu hiệu năng (inference speed) | **Tổng Phúc** | Báo cáo test, hệ thống ổn định |
| 6.5 | Chuẩn bị **video demo**, test case thực tế với ảnh lúa/cà phê thật | **Tuấn Anh** | Video demo, test cases |

### Kết quả cần đạt cuối Phase 6

| Hạng mục | Mô tả |
|----------|-------|
| Docker | Toàn bộ hệ thống chạy bằng `docker-compose up` |
| CI/CD | Auto deploy khi push lên main branch |
| Public URL | Hệ thống accessible từ internet (HTTPS) |
| Demo | Video demo + link ứng dụng |

---

## PHASE 7 — Viết Báo cáo & Chuẩn bị Bảo vệ
> 📅 **Tuần 11 → Tuần cuối** *(song song Phase 6)* | 🎯 Deadline nộp: **Tuần cuối (Nộp cuối kỳ)**

### Mục tiêu Phase 7
- Viết báo cáo PDF đầy đủ, chuyên nghiệp
- Chuẩn bị slide bảo vệ
- Đóng gói toàn bộ deliverables

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 7.1 | Viết phần **Giới thiệu, Bài toán, Dữ liệu** (Chương 1–2) | **Đàm Đạt** | Draft chương 1–2 |
| 7.2 | Viết phần **Tiền xử lý, EDA, Mô hình** (Chương 3–4) | **Xuân Trí** | Draft chương 3–4 |
| 7.3 | Viết phần **Đánh giá, Kết quả, Phân tích** (Chương 5) | **Tổng Phúc** | Draft chương 5 |
| 7.4 | Viết phần **Ứng dụng Web, Deployment** (Chương 6) | **Tuấn Anh** | Draft chương 6 |
| 7.5 | **Tổng hợp báo cáo**, viết Kết luận, chỉnh format, thiết kế Slide bảo vệ | **Anh Tuấn** | PDF báo cáo + PPTX slide |

### Kết quả cần đạt cuối Phase 7

| Hạng mục | Mô tả |
|----------|-------|
| Báo cáo PDF | Đầy đủ 7 bước quy trình, hình ảnh, bảng biểu |
| Slide PPTX | Rõ ràng, trực quan, phù hợp thời gian bảo vệ |
| Mã nguồn ZIP | Code sạch, có README, requirements |
| Model file | Checkpoint đã lưu (`.pt` / `.onnx` / `.pkl`) |

---

## Tổng kết phân công theo thành viên

| Thành viên | Phase chính phụ trách | Vai trò nổi bật |
|------------|----------------------|-----------------|
| **Anh Tuấn** | Phase 2, 3, 4, 5, 6, 7 | Quản lý dự án, Backend API, Swin Transformer, Tổng hợp báo cáo |
| **Xuân Trí** | Phase 2, 3, 4, 5, 6, 7 | MobileNetV2, Tuning, Frontend, CI/CD, Báo cáo phần EDA, mô hình |
| **Đàm Đạt** | Phase 1, 2, 3, 4, 5, 6, 7 | Xử lý dữ liệu, ResNet50, Error analysis, DB/Storage, Deploy |
| **Tổng Phúc** | Phase 2, 3, 4, 5, 6, 7 | Preprocessing, MLflow, Domain eval, Redis, Stress test |
| **Tuấn Anh** | Phase 1, 2, 3, 4, 5, 6, 7 | Tổng hợp tiến độ, DINOv2, Model ONNX, Integration, Video demo |

---

## Checklist Deliverables cuối kỳ

| # | Hạng mục | Người chịu trách nhiệm | Trạng thái |
|---|----------|------------------------|------------|
| 1 | Báo cáo (PDF) | Anh Tuấn (tổng hợp) | ⬜ |
| 2 | Mã nguồn (ZIP) | Anh Tuấn | ⬜ |
| 3 | Mô hình đã huấn luyện (`.pt`/`.onnx`) | Tuấn Anh | ⬜ |
| 4 | Slide bảo vệ (PDF/PPTX) | Anh Tuấn | ⬜ |
| 5 | Link ứng dụng web (Public URL) | Đàm Đạt | ⬜ |

---

## Quy tắc làm việc nhóm

- **Họp nhóm:** Ít nhất 1 lần/tuần (online hoặc offline)
- **Báo cáo tiến độ:** Cập nhật task trong repo mỗi cuối tuần
- **Code review:** Pull Request cần ít nhất 1 người approve trước khi merge
- **Tài liệu:** Viết tài liệu song song với code, không để đến cuối mới viết
- **Rủi ro & Escalation:** Nếu gặp khó khăn → báo nhóm trong vòng 24h để hỗ trợ kịp thời

---

*Cập nhật lần cuối: 2026-04-13*
