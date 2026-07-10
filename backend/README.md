# FastAPI Backend — Hướng dẫn cài đặt & Cơ sở dữ liệu

Tài liệu này hướng dẫn cách thiết lập cơ sở dữ liệu, kho lưu trữ MinIO và quản lý database migrations cho các thành viên phát triển Backend.

---

## 1. Kết quả thực hiện

Tui đã hoàn thành việc xây dựng và kiểm thử toàn bộ tầng dữ liệu và lưu trữ:
* **Tạo cấu trúc bảng (SQLModel)**: Thiết kế các bảng `users`, `images` và `predictions` hỗ trợ đăng ký, đăng nhập và lưu vết dự đoán cùng gợi ý chuyên gia.
* **Viết truy vấn (CRUD)**: Triển khai các hàm đăng ký tài khoản (băm mật khẩu trực tiếp qua bcrypt), kiểm tra đăng nhập, lưu log ảnh và kết quả dự đoán kèm theo phân trang lịch sử chẩn đoán.
* **Kho lưu trữ (MinIO)**: Hoàn thiện StorageService hỗ trợ kết nối, tự khởi tạo bucket, lưu ảnh ngầm dưới dạng stream bytes và xuất đường dẫn xem ảnh tạm thời (Presigned URL) bảo mật.
* **Đồng bộ hóa (Alembic)**: Cấu hình Alembic đọc kết nối động từ file cấu hình chung và sinh bản migration đầu tiên để khởi tạo bảng trên môi trường thật.

---

## 2. Truy cập môi trường đã deploy

Ứng dụng hiện đã được triển khai trên cloud qua DuckDNS:

* **Web App**: `https://plant-disease-demo.duckdns.org`
* **Backend API**: `https://plant-disease-demo.duckdns.org/api/v1`
* **Swagger UI**: `https://plant-disease-demo.duckdns.org/docs`

PostgreSQL, Redis và MinIO chạy như các service nội bộ trong cụm Kubernetes. MinIO Console không được public trực tiếp; nếu cần quản trị storage, dùng quyền truy cập hạ tầng hoặc port-forward theo runbook deploy.

## 3. Khởi chạy Dịch vụ phụ trợ cho phát triển cục bộ (Docker)

Để chạy PostgreSQL, MinIO và Redis phục vụ cho ứng dụng Backend cục bộ, hãy chạy lệnh sau từ thư mục gốc của dự án:

```bash
docker compose up -d postgres minio redis
```

* **PostgreSQL**: Chạy tại cổng 5432 (Username: `admin`, Password: `changeme`, Database: `plant_disease`).
* **MinIO API**: Chạy tại cổng 9000 (Access Key: `minioadmin`, Secret Key: `minioadmin`).
* **MinIO Console**: Chỉ dùng trong môi trường phát triển cục bộ; không public trong bản deploy cloud.

---

## 4. Quản lý Cơ sở dữ liệu (SQLModel & Alembic)

Dự án sử dụng SQLModel (wrapper trên SQLAlchemy 2.0) để định nghĩa Schema và quản lý dữ liệu.

### Cấu trúc bảng dữ liệu (backend/app/db/orm_models.py)
* `users`: Lưu tài khoản người dùng (`id`, `username`, `email`, `hashed_password`).
* `images`: Lưu metadata của ảnh tải lên MinIO (`id`, `user_id`, `object_key`, `original_filename`, `content_type`, `size_bytes`).
* `predictions`: Lưu kết quả chẩn đoán bệnh từ mô hình (`id`, `image_id`, `user_id`, `predicted_label`, `confidence`, `top_k`, `recommendation` dạng JSON, `latency_ms`).

### Lệnh chạy database migration (Alembic)
Các phiên bản schema được quản lý trong thư mục `backend/alembic/`. Khi khởi chạy dự án lần đầu hoặc khi deploy, hãy chạy lệnh sau để đồng bộ database:

```bash
# Áp dụng các thay đổi database lên PostgreSQL
uv run alembic upgrade head
```

Khi có thay đổi cấu trúc bảng trong `orm_models.py`, hãy chạy lệnh sau để tạo file migration mới:
```bash
uv run alembic revision --autogenerate -m "mô tả thay đổi"
```

---

## 5. Hướng dẫn sử dụng cho Backend Developer (Tuấn)

Phần DB & Storage đã được tích hợp và xuất khẩu sẵn tại `backend/app/db/__init__.py`. 
Ông có thể trực tiếp sử dụng như sau:

### Đăng ký, Đăng nhập và Truy vấn dữ liệu (crud.py)
```python
from backend.app.db import get_session
from backend.app.db import crud

# 1. Đăng ký người dùng mới (Mật khẩu tự động băm qua bcrypt trực tiếp)
user = crud.create_user(session, username="ten_user", email="email@abc.com", password="mat_khau_chua_hash")

# 2. Xác thực đăng nhập
is_valid = crud.verify_password("mat_khau_nhap_vao", user.hashed_password)

# 3. Ghi log kết quả dự đoán
crud.create_prediction_record(
    session=session,
    image_id=image_id,
    predicted_label="LeafBlast",
    confidence=0.92,
    top_k=[...]
)
```
*(Lưu ý: Hệ thống dùng trực tiếp thư viện bcrypt để băm mật khẩu, tránh lỗi phiên bản của thư viện passlib cũ trên Python 3.12).*

### Upload ảnh và hiển thị trên giao diện (storage.py)
Khi người dùng upload ảnh qua API `/predict`, hãy dùng StorageService để đẩy lên MinIO:

```python
from backend.app.services.storage import StorageService
from backend.app.config import settings

# Khởi tạo Service
storage = StorageService(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    bucket=settings.MINIO_BUCKET,
    secure=settings.MINIO_SECURE
)

# 1. Upload file ảnh nhận được từ API
object_key = storage.upload_image(file_bytes, filename="leaf.jpg", content_type="image/jpeg")

# 2. Lấy link hiển thị tạm thời (Presigned URL) có hạn 24 giờ gửi trả về Frontend
image_url = storage.get_url(object_key, expires_hours=24)
```
