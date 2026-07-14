# TÀI LIỆU NỘP BÀI ĐỒ ÁN CUỐI KỲ (SUBMISSION DELIVERABLES)

**Đồ án môn học:** Học Máy (Machine Learning)  
**Đề tài:** Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa  
**Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên  

---

## THÔNG TIN NHÓM THỰC HIỆN

| STT | Họ và tên | MSSV | Vai trò & Phân công chính |
|-----|-----------|------|---------------------------|
| 1 | Lê Xuân Trí | 23120099 | Thiết kế Kiến trúc Cloud (Docker, Kubernetes, k3s, GCP), Setup Storage (MinIO, PostgreSQL), Quản trị mã nguồn. |
| 2 | Đàm Tiến Đạt | 23120118 | Huấn luyện và Đánh giá Mô hình (YOLO26-seg, Mask R-CNN,...), Tối ưu hóa & Lượng tử hóa ONNX (Quantization), Model Card. |
| 3 | Tống Thanh Phúc | 23120158 | Xử lý thực nghiệm và Load Testing, Phân tích kết quả (Confusion Matrix, Error analysis), Quản trị Database. |
| 4 | Dương Tuấn Anh | 23120208 | Biên tập và xây dựng Video Demo sản phẩm, quay màn hình và thuyết minh tính năng hệ thống công khai. |
| 5 | Nguyễn Hồ Anh Tuấn | 23120185 | Chủ trì Báo cáo, viết Chương 1, tổng hợp và rà soát chất lượng nội dung Báo cáo, Slide, Backend API. |

---

## ĐƯỜNG DẪN TRIỂN KHAI CÔNG KHAI (PUBLIC DEPLOYMENT)

Hệ thống đã được đóng gói và triển khai thành công trên cụm Kubernetes (k3s) chạy trên máy ảo Google Cloud Platform (GCP) với các liên kết truy cập sau:

*   **Ứng dụng Web (Web App Frontend):** [https://plant-disease-demo.duckdns.org](https://plant-disease-demo.duckdns.org)
*   **Tài liệu API (Swagger UI):** [https://plant-disease-demo.duckdns.org/docs](https://plant-disease-demo.duckdns.org/docs)
*   **Cổng API Backend (Backend API):** [https://plant-disease-demo.duckdns.org/api/v1](https://plant-disease-demo.duckdns.org/api/v1)

---

## CẤU TRÚC THƯ MỤC NỘP BÀI (submission/)

Thư mục `submission/` được tổ chức một cách khoa học để giảng viên tiện kiểm tra và đánh giá:

```text
submission/
├── Report.pdf              # File Báo cáo đồ án hoàn chỉnh (PDF)
├── Slides.pdf              # File Slide trình bày cho buổi bảo vệ cuối kỳ (PDF)
├── code/                   # Thư mục chứa toàn bộ mã nguồn của hệ thống (đã dọn dẹp)
└── models/                 # Thư mục chứa mô hình học máy đã huấn luyện tốt nhất
    ├── yolo26_quantized.onnx  # File trọng số mô hình YOLO26-seg (định dạng ONNX quantized)
    └── class_names.json       # Ánh xạ chỉ mục lớp (class index) sang tên bệnh tiếng Việt
```

### Chi tiết các thành phần:

1.  **Báo cáo Đồ án (Report.pdf):** Trình bày chi tiết theo quy trình nghiên cứu khoa học End-to-End gồm 6 chương (từ định nghĩa bài toán, thu thập, tiền xử lý, phân tích dữ liệu EDA, huấn luyện, đánh giá mô hình, đến thiết kế hệ thống và triển khai thực tế).
2.  **Mã nguồn hệ thống (code/):** Gồm toàn bộ logic của:
    *   `crawl/`: Pipeline tự động crawl dữ liệu lá lúa & cà phê sử dụng `Crawl4AI` và giao diện bán tự động gán nhãn `Labeler.py` (Streamlit).
    *   `backend/`: API Backend xây dựng trên `FastAPI`, `SQLModel` (PostgreSQL), `MinIO` (quản lý ảnh), `Redis` (caching), và `ONNX Runtime` để chạy suy luận mô hình.
    *   `frontend/`: Giao diện Web Client viết bằng `Next.js` và `React` với phong cách thiết kế hiện đại, responsive.
    *   `deployment/`: Cấu hình Docker Compose và các tệp Helm Chart phục vụ triển khai Kubernetes.
    *   `notebooks/`: Các file Jupyter Notebook minh họa luồng tiền xử lý và quá trình huấn luyện mô hình (bao gồm `data_pipeline_demo.ipynb`, `eda.ipynb`, `model_training_evaluation.ipynb`).
3.  **Mô hình đã huấn luyện (models/):** File trọng số `yolo26_quantized.onnx` là mô hình phân vùng tốt nhất sau khi tối ưu và lượng tử hóa sang dạng INT8 giúp tăng tốc độ suy luận gấp 2.5 lần trên CPU nhưng vẫn giữ nguyên độ chính xác mAP.

---

## VIDEO DEMO SẢN PHẨM & LƯU TRỮ CLOUD

Do các file video chất lượng cao và các file trọng số mô hình gốc (`.pt`) có dung lượng lớn, nhóm đã lưu trữ và tổ chức chúng tại thư mục Google Drive dùng chung của môn học:

*   **Đường dẫn thư mục lưu trữ Cloud (Google Drive Shared Folder):** [Truy cập Google Drive](https://drive.google.com/drive/folders/1OS0M2uW8KuWymKMtZwIY8XMUGCBcBGwo?usp=sharing)
    *   *Thư mục chứa:* Video Demo hoàn chỉnh (`Video_Demo.mp4`), file trọng số gốc PyTorch (`yolo26_best.pt`), báo cáo và mã nguồn dự phòng.
    *   *Thời lượng Video Demo:* 4 phút 15 giây (Thuyết minh tiếng Việt giới thiệu đầy đủ luồng sử dụng ứng dụng web: Đăng nhập/Đăng ký, Upload chẩn đoán bệnh lá cà phê/lúa, xem lịch sử chẩn đoán, xem Cơ sở tri thức chuyên gia nông nghiệp).

---

## HƯỚNG DẪN CÀI ĐẶT & CHẠY THỬ CỤC BỘ (QUICK START)

Mã nguồn trong thư mục `code/` có cấu trúc hoàn toàn đồng bộ với repository. Giảng viên và người chấm có thể dễ dàng chạy thử theo các bước:

### 1. Yêu cầu hệ thống
*   Đã cài đặt Docker và Docker Compose.
*   (Tùy chọn) Đã cài đặt [uv](https://astral.sh/uv/) để quản lý môi trường ảo Python nhanh chóng.

### 2. Chuẩn bị Mô hình
Sao chép thư mục `models/` (bao gồm `yolo26_quantized.onnx` và `class_names.json`) trong thư mục submission này vào thư mục `code/models/`.

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

---

*Nhóm thực hiện đồ án xin chân thành cảm ơn thầy Bùi Tiến Lên đã đồng hành và hướng dẫn nhóm hoàn thành đồ án này!*
