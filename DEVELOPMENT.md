# 🌿 Hướng dẫn Cài đặt & Chạy Web (Development)

Tài liệu này hướng dẫn cách cài đặt dependencies và chạy toàn bộ hệ thống web (frontend + backend) trên máy local.

---

## 🚀 Chạy toàn bộ stack bằng Docker (khuyến nghị)

Đây là cách nhanh nhất — **chỉ cần 1 lệnh** để khởi động toàn bộ hệ thống:

```bash
# Bước 1: Đảm bảo Docker Desktop đang chạy, rồi chạy lệnh này từ thư mục gốc
docker compose up --build
```

Lệnh này sẽ tự động:
- Build Docker image cho **frontend** (Next.js) và **backend** (FastAPI)
- Khởi động **PostgreSQL**, **MinIO**, **Redis**
- Chạy **database migration** (alembic) trước khi backend start
- Kết nối tất cả services với nhau qua Docker network

**Sau khi khởi động xong, truy cập:**

| Dịch vụ | URL |
|---------|-----|
| 🌐 Web App | http://localhost:3000 |
| 📖 API Docs | http://localhost:8000/docs |
| 🗂️ MinIO Console | http://localhost:9001 |

**Các lệnh hữu ích khác:**

```bash
# Chạy nền (không block terminal)
docker compose up --build -d

# Xem logs
docker compose logs -f

# Xem logs của 1 service cụ thể
docker compose logs -f backend

# Dừng tất cả
docker compose down

# Dừng và xóa volumes (reset database)
docker compose down -v
```

> **Lưu ý:** Lần đầu build sẽ mất ~5–10 phút do phải tải dependencies. Các lần sau sẽ nhanh hơn nhờ Docker cache.

---

## 📋 Yêu cầu hệ thống

| Công cụ | Phiên bản tối thiểu | Mục đích |
|---------|---------------------|----------|
| [Python](https://python.org) | 3.12+ | Backend FastAPI |
| [uv](https://docs.astral.sh/uv/) | mới nhất | Quản lý Python packages |
| [Node.js](https://nodejs.org) | 18+ | Frontend Next.js |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | mới nhất | PostgreSQL, MinIO, Redis |

---

## ⚙️ Bước 1 — Cài đặt Dependencies

### 1.1 Backend (Python)

Cài `uv` nếu chưa có:

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Sync Python packages:

```bash
uv sync
```

### 1.2 Frontend (Node.js)

```bash
cd frontend
npm install
cd ..
```

---

## 🐳 Bước 2 — Khởi động Services (Docker)

> **Lưu ý:** Mở **Docker Desktop** trước và đảm bảo nó đang chạy (icon cá voi ổn định trong system tray).

### 2.1 Kiểm tra Docker đang hoạt động

```bash
docker ps
```

Nếu lỗi `failed to connect to the docker API`, hãy chờ thêm ~30s cho Docker Desktop khởi động hoàn toàn.

### 2.2 Khởi động PostgreSQL, MinIO, Redis

```bash
docker compose up -d postgres minio redis
```

Kiểm tra các containers đang chạy:

```bash
docker compose ps
```

Kết quả mong đợi:
```
NAME                    STATUS          PORTS
deployment-postgres-1   Up (healthy)    0.0.0.0:5433->5432/tcp
deployment-redis-1      Up (healthy)    0.0.0.0:6379->6379/tcp
deployment-minio-1      Up (healthy)    0.0.0.0:9000-9001->9000-9001/tcp
```

> **⚠️ Lưu ý Port Postgres:** PostgreSQL Docker dùng port **5433** (không phải 5432) để tránh xung đột với PostgreSQL cài nội địa trên Windows.

---

## 🔑 Bước 3 — Cấu hình Environment Variables

Tạo file `.env` ở **thư mục gốc** của dự án bằng cách copy từ template:

```bash
cp backend/.env.example .env
```

Sau đó chỉnh sửa file `.env` với nội dung sau (cho môi trường local):

```dotenv
APP_ENV=development
MODEL_PATH=models/yolo26_quantized.onnx
CLASS_NAMES_PATH=models/class_names.json
MODEL_INPUT_SIZE=640
MODEL_VERSION=yolo26-seg-onnx
SKIP_DB_INIT=false

SECRET_KEY=change-me-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440

POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5433
POSTGRES_DB=plant_disease
POSTGRES_USER=admin
POSTGRES_PASSWORD=changeme

REDIS_URL=redis://127.0.0.1:6379/0

MINIO_ENDPOINT=127.0.0.1:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=plant-disease-images
MINIO_SECURE=false

MLFLOW_TRACKING_URI=http://127.0.0.1:5000
```

> **Quan trọng:** Dùng `127.0.0.1` thay vì `localhost` để tránh psycopg2 kết nối qua IPv6 (`::1`).

---

## 🗄️ Bước 4 — Khởi tạo Database

Chạy migration để tạo các bảng trong PostgreSQL:

```bash
uv run alembic upgrade head
```

Kết quả mong đợi:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 5d9babedd663, initial_schema
```

---

## 🚀 Bước 5 — Chạy Backend (FastAPI)

```bash
uv run uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend sẽ khởi động tại `http://localhost:8000`. Kiểm tra:
- **API Docs (Swagger):** http://localhost:8000/docs
- **Health check:** http://localhost:8000/health

---

## 🌐 Bước 6 — Chạy Frontend (Next.js)

Mở terminal **mới** (backend vẫn chạy ở terminal cũ):

```bash
cd frontend
npm run dev
```

Frontend sẽ khởi động tại `http://localhost:3000`.

---

## ✅ Truy cập Web

Sau khi cả hai server đang chạy:

| Dịch vụ | URL | Ghi chú |
|---------|-----|---------|
| **Web App** | http://localhost:3000 | Giao diện chính |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **MinIO Console** | http://localhost:9001 | Quản lý file ảnh (user: `minioadmin` / pass: `minioadmin`) |

---

## 🧪 Test Nhanh

1. Mở http://localhost:3000
2. Click **"+ Chẩn đoán mới"** hoặc dùng ô upload ở trang chính
3. Click icon 📎 (đính kèm) và chọn ảnh lá cây (định dạng `.jpg`, `.png`, `.webp`)
4. Nhấn nút **gửi** (mũi tên →) để bắt đầu chẩn đoán
5. Kết quả sẽ hiển thị: tên bệnh, độ tin cậy, khuyến nghị điều trị

---

## 🛑 Dừng các Services

```bash
# Dừng frontend: Ctrl+C trong terminal đang chạy npm run dev
# Dừng backend:  Ctrl+C trong terminal đang chạy uvicorn

# Dừng Docker containers
docker compose down
```

---

## 🔧 Xử lý sự cố thường gặp

### ❌ Docker không kết nối được
```
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
```
**Giải pháp:** Docker Desktop chưa khởi động xong. Chờ thêm 30–60 giây rồi thử lại.

---

### ❌ PostgreSQL lỗi authentication
```
FATAL: password authentication failed for user "admin"
```
**Giải pháp:** Máy có PostgreSQL cài nội địa đang chạy trên port 5432. File `.env` đã được cấu hình dùng port `5433` (Docker postgres). Đảm bảo `POSTGRES_PORT=5433` trong file `.env`.

---

### ❌ Frontend lỗi "Failed to fetch"
**Giải pháp:** Backend chưa chạy. Đảm bảo chạy `uvicorn` ở Bước 5 trước khi dùng web.

---

### ❌ Model không tìm thấy
```
Model file not found: models/yolo26_quantized.onnx
```
**Giải pháp:** File model ONNX cần được đặt tại `models/yolo26_quantized.onnx` và `models/class_names.json`. Liên hệ team ML để lấy file model đã train.

---

## 📁 Cấu trúc dự án (tóm tắt)

```
ml-vietnam-plant-disease-detection/
├── frontend/               # Next.js web app
│   ├── src/                # Source code
│   └── package.json        # Node dependencies
├── backend/
│   ├── app/                # FastAPI application
│   │   ├── main.py         # Entry point
│   │   ├── config.py       # Cấu hình (đọc từ .env)
│   │   ├── routers/        # API endpoints
│   │   └── services/       # Business logic (predict, storage...)
│   └── alembic/            # Database migrations
├── deployment/
│   └── docker-compose.yml  # Docker services config
├── models/                 # File model ONNX (không commit lên git)
├── data/                   # Dataset
├── .env                    # ⚠️ Tạo thủ công, không commit lên git
└── pyproject.toml          # Python dependencies
```
