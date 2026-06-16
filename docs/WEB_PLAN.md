# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ - WEB & DEVOPS PHASE
## Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa

## TRẠNG THÁI CHUẨN BỊ

**Lựa chọn mô hình Deploy**: Thống nhất chọn **YOLO26-seg** (dựa trên YOLOv8-seg) làm mô hình chính thức để tích hợp vào ứng dụng.

---

## Tổng quan mốc thời gian (Web & DevOps Phase)

| Deadline | Phase | Nội dung yêu cầu nộp | Trạng thái |
|----------|-------|----------------------|------------|
| 28/6 | 5 | **Xây dựng Ứng dụng (Frontend, Backend, Database)** | Chưa thực hiện |
| 5/7 | 6 | **Triển khai & DevOps (K8s, CI/CD, Helm, Traefik)** | Chưa thực hiện |

---

## PHASE 5 — Xây dựng Ứng dụng
> **Deadline: 28/6**

### Mục tiêu Phase 5
- Tối ưu hóa mô hình YOLO26-seg: Tune hoàn thiện, export sang ONNX và thực hiện Quantization.
- Xây dựng Backend bằng FastAPI với các API `/predict`, `/auth`, `/history`.
- Xây dựng Database bằng Python sử dụng **SQLModel** để kết nối DB, thực hiện các truy vấn lưu thông tin user, kết quả model, và URL ảnh trong MinIO. Thiết lập và cấu hình MinIO để lưu trữ ảnh người dùng.
- Xây dựng Frontend: Dùng Next.js hoặc sử dụng Google AI Studio tạo prototype nhanh, sau đó đưa về local dùng Agent (như Antigravity/Codex/Claude Code) hỗ trợ gắn kết nối API giữa Frontend và Backend.
- Tích hợp Expert Knowledge Base tiếng Việt cung cấp hướng dẫn xử lý bệnh.

### Phân công công việc Phase 5

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 5.1 | **Model Preparation**: Tune hoàn thiện, export sang định dạng ONNX, thực hiện Quantization cho mô hình YOLO26-seg để tối ưu hóa suy luận trên CPU. | **Đàm Tiến Đạt** | `models/yolo26_quantized.onnx`, script export & quantize |
| 5.2 | **Backend FastAPI**: Phát triển API FastAPI (`/predict`, login/register, `/history`), tích hợp logic gọi model qua ONNX Runtime và kết nối database. | **Nguyễn Hồ Anh Tuấn** | `backend/app/`, Dockerfile backend |
| 5.3 | **Database & MinIO**: Viết code Python dùng SQLModel kết nối DB + viết truy vấn (lưu thông tin user, kết quả model, URL ảnh trong MinIO) + Setup cài đặt MinIO để lưu ảnh người dùng. | **Tống Thanh Phúc** | SQLModel schemas, DB queries, MinIO configuration |
| 5.4 | **Frontend App**: Phát triển giao diện (Next.js hoặc prototype từ Google AI Studio mang về local dùng Agent sửa code kết nối backend), hỗ trợ giao diện mobile-first trực quan. | **Dương Tuấn Anh** | `frontend/`, UI demo kết nối backend |
| 5.5 | **Expert Knowledge Base & API Specs**: Thiết kế module gợi ý xử lý bệnh theo luật chuyên gia (tiếng Việt), xây dựng tài liệu Swagger/OpenAPI spec cho toàn hệ thống. | **Lê Xuân Trí** | `backend/app/knowledge/`, OpenAPI documentation |

## USE CASES CỦA ỨNG DỤNG

Ứng dụng hướng đến trải nghiệm người dùng cuối trực quan và đơn giản:
1. **Đăng ký & Đăng nhập**: Người dùng đăng ký tài khoản mới và đăng nhập để quản lý lịch sử chẩn đoán.
2. **Chẩn đoán & Gợi ý xử lý**:
   - Người dùng chụp ảnh trực tiếp từ camera hoặc tải ảnh lá cây lên.
   - Hệ thống chạy mô hình YOLO26-seg dự đoán bệnh.
   - Hiển thị kết quả chẩn đoán kèm gợi ý cách xử lý/phòng ngừa phù hợp (Expert Knowledge Base).
3. **Xem lại lịch sử**: Người dùng xem lại toàn bộ ảnh đã chụp cùng kết quả chẩn đoán và gợi ý xử lý của hệ thống trước đó.

---

### Kiến trúc hệ thống

```
User (Browser/Mobile)
  └─→ Frontend (Next.js / AI Studio Prototype)
         └─→ API Request (Auth/Predict/History) → Backend (FastAPI)
                                                     ├── MinIO (Lưu ảnh người dùng)
                                                     ├── ONNX Runtime (Chạy model YOLO26-seg quantized)
                                                     ├── Knowledge Base (Luật chuyên gia tiếng Việt)
                                                     └── Database (PostgreSQL/MySQL qua SQLModel)
```

### Kết quả cần đạt cuối Phase 5

| Hạng mục | Mô tả |
|----------|-------|
| ONNX Model | YOLO26-seg được quantize thành công, inference tốc độ cao trên CPU |
| Backend API | FastAPI chạy ổn định với đầy đủ các endpoint yêu cầu, có Swagger docs |
| Database & MinIO | SQLModel kết nối trơn tru, lưu thông tin đầy đủ, MinIO lưu ảnh thành công |
| Frontend | Giao diện thân thiện, tương tác tốt với backend, hiển thị kết quả chẩn đoán & gợi ý xử lý |

---

## PHASE 6 — Triển khai & DevOps
> **Deadline: 5/7**
>
> *Lưu ý cấu hình tài nguyên: Thường thì sẽ không bị quá tải/thiếu bộ nhớ vì YOLO rất nhẹ. Tuy nhiên, lúc setup cluster thì nên chọn machine type có khoảng 8GB RAM. Backend thì cấu hình Pod Limit cao khoảng 7GB để đảm bảo hoạt động mượt mà.*

### Mục tiêu Phase 6
- Containerize toàn bộ các service của ứng dụng.
- Thiết lập Kubernetes cluster (thực hiện thủ công cho đơn giản hoặc dùng Terraform).
- Xây dựng CI/CD pipeline bằng GitHub Actions: tự động chạy test -> build Docker image -> deploy lên K8s thông qua Helm Chart.
- Thiết lập DuckDNS + Traefik/Nginx để định tuyến request từ ngoài internet vào ứng dụng.
- Thực hiện E2E integration testing và load testing.

### Phân công công việc Phase 6

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 6.1 | **Kubernetes Setup**: Cài đặt cụm Kubernetes cluster (thủ công cho đơn giản hoặc dùng Terraform nếu thành thạo) để quản lý container. | **Lê Xuân Trí** | Kubernetes cluster cấu hình thành công |
| 6.2 | **CI/CD Pipeline**: Viết GitHub Actions workflow tự động chạy test, build Docker images và đẩy lên registry. | **Lê Xuân Trí** | `.github/workflows/ci.yml` |
| 6.3 | **Helm Chart Deployment**: Tạo Helm Chart cho các service (Frontend, Backend, DB, MinIO) để deploy tự động lên Kubernetes cluster. | **Lê Xuân Trí** | `deployment/helm/` |
| 6.4 | **DuckDNS & Traefik/Nginx Ingress**: Cấu hình tên miền động DuckDNS và cài đặt Traefik/Nginx Ingress để định tuyến request HTTPS từ user đến app. | **Lê Xuân Trí** | Cấu hình Ingress, tên miền hoạt động |
| 6.5 | **Model Serving on K8s**: Tối ưu hóa việc deploy mô hình YOLO26-seg quantized trên K8s, tích hợp ONNX Runtime trong backend pod. | **Đàm Tiến Đạt** | Deployment config cho Model serving |
| 6.6 | **Integration & Load Testing**: Viết và chạy test tích hợp E2E (login -> upload ảnh -> nhận kết quả) cùng kịch bản load test kiểm tra độ chịu tải. | **Nguyễn Hồ Anh Tuấn** & **Tống Thanh Phúc** | `tests/`, test reports |
| 6.7 | **Database & Storage Scaling**: Cấu hình persistent volume cho Database và MinIO trên cụm Kubernetes, đảm bảo tính toàn vẹn dữ liệu. | **Tống Thanh Phúc** & **Dương Tuấn Anh** | K8s PVC configs |

### Stack triển khai

| Thành phần | Vai trò |
|---|---|
| Kubernetes | Quản lý và điều phối các containers của hệ thống |
| Helm Chart | Đóng gói và deploy ứng dụng lên Kubernetes dễ dàng |
| GitHub Actions | CI/CD tự động hóa quy trình test, build và deploy |
| Traefik / Nginx | Ingress controller điều hướng traffic và cấu hình HTTPS SSL |
| DuckDNS | Cung cấp tên miền miễn phí ánh xạ tới IP của cluster |
| Docker | Đóng gói các dịch vụ thành image |
| ONNX Runtime | Engine chạy mô hình YOLO26-seg đã quantize trên CPU |

### Kết quả cần đạt cuối Phase 6

| Hạng mục | Mô tả |
|----------|-------|
| Kubernetes Cluster | Các pods (FastAPI, Frontend, DB, MinIO) chạy ổn định trên K8s |
| CI/CD & Helm | Chỉ cần push code mới -> Tự động hóa build & deploy lên K8s qua Helm |
| URL truy cập | Người dùng truy cập app bình thường thông qua domain DuckDNS có HTTPS |
| Verification | Hệ thống vượt qua các bài kiểm tra E2E và chịu tải cơ bản |

---

## Đề xuất Điểm Sáng Tạo liên quan đến Web, App & DevOps

| # | Ý tưởng sáng tạo | Phase | Người phụ trách | Giá trị mang lại |
|---|-----------------|-------|-----------------|-----------------|
| S1 | **Expert Knowledge Base** tiếng Việt: luật chuyên gia động, gợi ý trực quan giải pháp phòng bệnh phù hợp cho nông dân | 5 | **Lê Xuân Trí** | Giá trị ứng dụng thực tiễn cao, hỗ trợ người nông dân trực tiếp |
| S2 | **Triển khai GitOps/DevOps nâng cao**: Sử dụng Kubernetes kết hợp Helm Chart và CI/CD hoàn chỉnh trên môi trường Cloud | 6 | **Lê Xuân Trí** | Mô hình triển khai doanh nghiệp thực tế, dễ nâng cấp và mở rộng |

---

## Tổng hợp phân công công việc (Web & DevOps Phase)

| Thành viên | Phase 5 (Xây dựng Ứng dụng) | Phase 6 (Triển khai & DevOps) | Vai trò chính |
|-----------|-------------------------|---------------------------|--------------|
| **Lê Xuân Trí** | Expert Knowledge Base & API Specs (5.5) | K8s Setup, CI/CD, Helm, Traefik (6.1, 6.2, 6.3, 6.4) | **DevOps & Knowledge Lead** |
| **Đàm Tiến Đạt** | Model Prep (Tune, ONNX, Quantize) (5.1) | Model Serving on K8s (6.5) | **Machine Learning Engineer** |
| **Tống Thanh Phúc** | Database SQLModel & MinIO (5.3) | Load Testing & Storage Scaling (6.6, 6.7) | **Database & QC Engineer** |
| **Dương Tuấn Anh** | Frontend App Integration (5.4) | Storage Scaling & Logs (6.7) | **Frontend Developer** |
| **Nguyễn Hồ Anh Tuấn** | Backend FastAPI Development (5.2) | Integration Testing (6.6) | **Backend & QC Developer** |
