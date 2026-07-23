# MÃ NGUỒN HỆ THỐNG (code/)

Thư mục này chứa toàn bộ mã nguồn của hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (cà phê và lúa).

## CẤU TRÚC THƯ MỤC & TỆP TIN

Dưới đây là chi tiết các thành phần chính nằm trong thư mục `code/`:

### Các thư mục chức năng chính:
- **`backend/`**: Mã nguồn API Backend được xây dựng bằng **FastAPI** và **SQLModel** (kết nối PostgreSQL). Sử dụng **MinIO** để quản lý lưu trữ hình ảnh, **Redis** cho việc lưu trữ bộ nhớ đệm (caching), và **ONNX Runtime** để chạy suy luận mô hình phân vùng thực thể (segmentation inference).
- **`frontend/`**: Giao diện Web Client được xây dựng với **Next.js** và **React** hỗ trợ người dùng tải ảnh lên và xem chẩn đoán bệnh.
- **`crawl/`**: Chứa công cụ tự động thu thập dữ liệu ảnh từ web bằng **Crawl4AI** và giao diện bán tự động hỗ trợ gán nhãn thực thể **Labeler.py** (chạy bằng Streamlit).
- **`deployment/`**: Thư mục chứa cấu hình Docker Compose và các tệp Helm Chart phục vụ triển khai ứng dụng trên môi trường Kubernetes (k3s).
- **`notebooks/`**: Các Jupyter Notebook nghiên cứu phát triển:
  - `01_eda.ipynb`: Phân tích khám phá dữ liệu (EDA) tập dữ liệu bệnh lá lúa và lá cà phê.
  - `02_preprocessing.ipynb`: Tiền xử lý dữ liệu và tạo mặt nạ nhãn (masks).
  - `models/`: Thư mục chứa các Jupyter Notebook phục vụ việc xây dựng, huấn luyện và đánh giá các kiến trúc mô hình khác nhau (YOLOv8-Seg, Mask R-CNN, Mask2Former, Real-time DETR, MobileSAM) cho hai loại cây trồng.
- **`src/`**: Mã nguồn lõi Python phục vụ cho huấn luyện mô hình:
  - `data/`: Các tiện ích xử lý dữ liệu đầu vào.
  - `segmentation/`: Logic chuẩn bị dữ liệu, cấu hình huấn luyện và kiểm thử mô hình.
  - `utils/`: Thư viện tiện ích dùng chung (ghi log, trực quan hóa mặt nạ phân vùng, đo đạc chỉ số).
- **`scripts/`**: Các script hỗ trợ tự động hóa như: xuất cấu hình OpenAPI (`export_openapi.py`), xuất mô hình PyTorch sang ONNX (`export_onnx.py`), kiểm tra và hiển thị các mặt nạ gán nhãn (`check_masks.py`, `show_masks.py`), và vẽ sơ đồ kiến trúc.
- **`tests/`**: Các bài kiểm thử tích hợp (integration tests), kiểm thử hiệu năng (load tests) và kiểm thử chất lượng API.
- **`models/`**: Thư mục chứa các mô hình đã huấn luyện (định dạng ONNX/PyTorch). *Lưu ý: Cần sao chép các file mô hình từ thư mục `/models` ở thư mục gốc của gói nộp bài vào đây khi chạy thử cục bộ.*

### Các tệp cấu hình:
- **`docker-compose.yml`**: Tệp cấu hình Docker Compose để khởi chạy nhanh toàn bộ các dịch vụ (Backend, Frontend, DB, MinIO, Redis) cục bộ.
- **`pyproject.toml` & `uv.lock`**: Các file quản lý môi trường ảo và dependencies dự án thông qua công cụ quản lý package **uv**.
- **`alembic.ini`**: File cấu hình migration cho cơ sở dữ liệu PostgreSQL sử dụng Alembic.
- **`.env`**: File mẫu chứa các biến môi trường cấu hình hệ thống (như kết nối DB, API Key, cấu hình MinIO/Redis).
- **`.gitignore`**: Định nghĩa các file và thư mục bỏ qua không đưa lên Git repository.
- **`.python-version`**: Xác định phiên bản Python tối thiểu yêu cầu cho dự án.
