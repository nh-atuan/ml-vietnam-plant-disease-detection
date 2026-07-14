# HỆ THỐNG PHÂN VÙNG THỰC THỂ CHẨN ĐOÁN BỆNH TRÊN LÁ CÂY NÔNG NGHIỆP ĐẶC SẢN CÀ PHÊ VÀ LÚA

**Đồ án môn học:** Học Máy (Machine Learning)  
**Đề tài:** Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa  
**Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên  

---

## THÔNG TIN NHÓM THỰC HIỆN

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Lê Xuân Trí | 23120099 |
| 2 | Đàm Tiến Đạt | 23120118 |
| 3 | Tống Thanh Phúc | 23120158 |
| 4 | Dương Tuấn Anh | 23120208 |
| 5 | Nguyễn Hồ Anh Tuấn | 23120185 |

---

## ĐƯỜNG DẪN TRIỂN KHAI CÔNG KHAI (PUBLIC DEPLOYMENT)

Hệ thống đã được đóng gói và triển khai thành công trên cụm Kubernetes (k3s) chạy trên máy ảo Google Cloud Platform (GCP) với các liên kết truy cập sau:

*   **Ứng dụng Web (Web App Frontend):** [https://plant-disease-demo.duckdns.org](https://plant-disease-demo.duckdns.org)
*   **Tài liệu API (Swagger UI):** [https://plant-disease-demo.duckdns.org/docs](https://plant-disease-demo.duckdns.org/docs)
*   **Cổng API Backend (Backend API):** [https://plant-disease-demo.duckdns.org/api/v1](https://plant-disease-demo.duckdns.org/api/v1)

---

## CẤU TRÚC THƯ MỤC NỘP BÀI

Thư mục được tổ chức một cách khoa học để giảng viên tiện kiểm tra và đánh giá:

```text
.
├── Report.pdf              # File Báo cáo đồ án hoàn chỉnh (PDF)
├── Slides.pdf              # File Slide trình bày cho buổi bảo vệ cuối kỳ (PDF)
├── code/                   # Thư mục chứa toàn bộ mã nguồn của hệ thống
└── models/                 # Thư mục chứa mô hình học máy đã huấn luyện tốt nhất
```

### Chi tiết các thành phần:

1.  **Báo cáo Đồ án (Report.pdf):** Trình bày chi tiết theo quy trình nghiên cứu khoa học End-to-End gồm 6 chương (từ định nghĩa bài toán, thu thập, tiền xử lý, phân tích dữ liệu EDA, huấn luyện, đánh giá mô hình, đến thiết kế hệ thống và triển khai thực tế).
2.  **Mã nguồn hệ thống (code/):** Gồm toàn bộ logic của:
    *   `crawl/`: Pipeline tự động crawl dữ liệu lá lúa & cà phê sử dụng `Crawl4AI` và giao diện bán tự động gán nhãn `Labeler.py` (Streamlit).
    *   `backend/`: API Backend xây dựng trên `FastAPI`, `SQLModel` (PostgreSQL), `MinIO` (quản lý ảnh), `Redis` (caching), và `ONNX Runtime` để chạy suy luận mô hình.
    *   `frontend/`: Giao diện Web Client viết bằng `Next.js` và `React` với phong cách thiết kế hiện đại, responsive.
    *   `deployment/`: Cấu hình Docker Compose và các tệp Helm Chart phục vụ triển khai Kubernetes.
    *   `notebooks/`: Các file Jupyter Notebook minh họa luồng tiền xử lý và quá trình huấn luyện mô hình (bao gồm `data_pipeline_demo.ipynb`, `eda.ipynb`, `model_training_evaluation.ipynb`).
3.  **Mô hình đã huấn luyện (models/):** Thư mục chứa mô hình học máy đã huấn luyện tốt nhất.

---

## VIDEO DEMO SẢN PHẨM & LƯU TRỮ CLOUD

---

## HƯỚNG DẪN CÀI ĐẶT & CHẠY THỬ CỤC BỘ (QUICK START)

Mã nguồn trong thư mục `code/` có cấu trúc hoàn toàn đồng bộ với repository. Có thể dễ dàng chạy thử theo các bước:

### 1. Yêu cầu hệ thống
*   Đã cài đặt Docker và Docker Compose.
*   (Tùy chọn) Đã cài đặt [uv](https://astral.sh/uv/) để quản lý môi trường ảo Python nhanh chóng.

### 2. Chuẩn bị Mô hình
Sao chép thư mục `models/` ở thư mục gốc vào thư mục `code/models/`.

### 3. Chạy toàn bộ hệ thống bằng Docker Compose
Tại thư mục `code/`:
```bash
docker-compose up --build
```
Lệnh này sẽ tự động khởi dựng và liên kết:
*   Database PostgreSQL tại cổng `5433`
*   Object Storage MinIO tại cổng `9000` (Console tại cổng `9001`)
*   Redis Caching tại cổng `6379`
*   FastAPI Backend Server tại cổng `8000`
*   Next.js Frontend Client tại cổng `3000`

Sau khi khởi chạy thành công, truy cập giao diện web cục bộ tại địa chỉ [http://localhost:3000](http://localhost:3000).
