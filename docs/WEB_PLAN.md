# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ - WEB & DEVOPS PHASE
## Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa

---

## GIAI ĐOẠN CHUẨN BỊ (Trước khi thực hiện Phase 5 & 6)
> **Kế hoạch chạy lại Notebook & Đo đạc Inference Time trên CPU**

Trước khi bắt tay vào xây dựng ứng dụng (Phase 5) và triển khai (Phase 6), tất cả thành viên trong nhóm cần thực hiện một bước chuẩn bị bắt buộc nhằm đảm bảo mô hình hoạt động ổn định và sẵn sàng cho việc tích hợp vào hệ thống web:

### 1. Kế hoạch chạy lại Notebook
Mỗi thành viên chịu trách nhiệm chạy lại **2 notebook huấn luyện** (ứng với tập dữ liệu Rice và Coffee) của mô hình mình phụ trách (đã được phân công từ Model Phase):
*   **Lê Xuân Trí:** Mask R-CNN
*   **Nguyễn Hồ Anh Tuấn:** YOLO26-seg
*   **Tống Thanh Phúc:** RF-DETR
*   **Đàm Tiến Đạt:** MobileSAM
*   **Dương Tuấn Anh:** Mask2Former

### 2. Đo đạc Inference Time trên CPU 

**Đo thời gian suy luận (Inference Time) bắt buộc phải thực hiện trên CPU.**

**Tại sao cần đo trên CPU?** Khi đưa mô hình lên web serving ở Phase 5 & 6 (sử dụng FastAPI và ONNX Runtime), hệ thống sẽ chạy chủ yếu trên môi trường CPU của server deploy để tiết kiệm chi phí và tài nguyên (thường không có GPU hoặc GPU bị giới hạn). Do đó, tốc độ suy luận thực tế trên CPU mới là chỉ số quyết định hiệu năng của ứng dụng.

**Yêu cầu kỹ thuật:** Trong notebook chạy lại, cần bổ sung đoạn code đo thời gian xử lý trung bình trên CPU cho một mẫu ảnh (tính bằng mili-giây - ms) khi thực hiện dự đoán đầy đủ (từ tiền xử lý, chạy mô hình, đến hậu xử lý tạo mask).

**Đầu ra:** Upload lạy 2 notebooks với ouput mới sau khi thực hiện. Ghi nhận và báo cáo cụ thể chỉ số này vào file README.md tương ứng để làm cơ sở so sánh chọn ra model tốt nhất và tối ưu hóa khi chuyển đổi sang định dạng ONNX.

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

## Tổng quan mốc thời gian (Web & DevOps Phase)

| Mốc | Thời điểm | Phase | Nội dung yêu cầu nộp | Trạng thái |
|-----|-----------|-------|----------------------|------------|
| Tuần 10–12 | Ứng dụng | 5 | **Xây dựng Ứng dụng** – ONNX export, Backend FastAPI, Frontend Next.js | Chưa thực hiện |
| Tuần 12–13 | DevOps | 6 | **Triển khai & DevOps** – Docker Compose, CI/CD, DuckDNS, URL công khai | Chưa thực hiện |

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
| 5.2 | **Backend FastAPI**: REST API `/predict` (nhận ảnh → trả nhãn + top-k + confidence), kết nối PostgreSQL (log dự đoán), MinIO (lưu ảnh gốc), Redis (cache kết quả TTL 1h), Swagger docs | **Tuấn Anh** | `backend/app/`, Docker service backend |
| 5.3 | **Frontend Next.js**: trang upload ảnh, hiển thị kết quả chẩn đoán (nhãn, confidence, top-k, gợi ý xử lý), giao diện mobile-first responsive | **Đàm Đạt** | `frontend/`, UI demo hoạt động |
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
| 6.3 | **DuckDNS + Traefik**: cấu hình tên miền động, HTTPS auto (Let's Encrypt), reverse proxy routing | **Tuấn Anh** | `deployment/traefik/`, URL demo công khai |
| 6.4 | **MLOps Dashboard**: tích hợp MLflow UI vào hệ thống deploy, model versioning & experiment comparison | **Tống Phúc** | MLflow service trong Docker Compose |
| 6.5 | **Integration testing**: end-to-end test pipeline (upload ảnh → predict → verify response), load test cơ bản | **Anh Tuấn** | `tests/`, test scripts |
| 6.6 | **SAM 3 Segmentation**: pseudo-mask generation cho ảnh nhiều lá, tích hợp optional vào API `/segment` | **Tuấn Anh** | `src/segmentation/`, endpoint bổ sung |

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

## Đề xuất Điểm Sáng Tạo liên quan đến Web, App & DevOps

| # | Ý tưởng sáng tạo | Phase | Người phụ trách | Giá trị mang lại |
|---|-----------------|-------|-----------------|-----------------|
| S3 | **Expert Knowledge Base** tiếng Việt: gợi ý xử lý bệnh theo luật chuyên gia, hành động cụ thể cho nông dân | 5 | **Xuân Trí** | Giá trị ứng dụng thực tiễn cao, bối cảnh Việt Nam |
| S6 | **MLOps Dashboard**: tích hợp MLflow UI vào hệ thống deploy, theo dõi model versioning & experiment comparison trực tiếp | 6 | **Tống Phúc** | Quy trình MLOps chuyên nghiệp, dễ mở rộng |

---

## Tổng hợp công việc (Web & DevOps Phase)

| Thành viên | Phase 5 | Phase 6 | Sáng tạo |
|-----------|---------|---------|----------|
| **Lê Xuân Trí** | Knowledge Base (5.4) | — | S3 |
| **Đàm Tiến Đạt** | Frontend (5.3) | — | — |
| **Tống Thanh Phúc** | DB Schema (5.5) | Docker/CI-CD (6.1, 6.2), MLOps (6.4) | S6 |
| **Dương Tuấn Anh** | Backend FastAPI (5.2) | DuckDNS/Traefik (6.3), SAM 3 (6.6) | — |
| **Nguyễn Hồ Anh Tuấn** | Model Export (5.1) | Integration Test (6.5) | — |

---

## Checklist skeleton theo output (Web & DevOps Phase)

| Phase | Output chính | Skeleton trong repo |
|---|---|---|
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
