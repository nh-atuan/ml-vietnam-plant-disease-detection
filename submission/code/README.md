# Tài liệu Diễn giải Thư mục Mã nguồn Dự án (`code/`)

Tài liệu này dùng để diễn giải chi tiết cấu trúc, vai trò và chức năng của từng file, thư mục, module có trong mã nguồn dự án **"Hệ thống Phân vùng Thực thể Chẩn đoán Bệnh trên Lá cây Nông nghiệp Đặc sản (Cà phê & Lúa)"**.

---

## 1. Cấu trúc Tổng quan Thư mục (`code/`)

```text
code/
├── backend/                  # FastAPI Web Service & Engine Suy luận Mô hình (ONNX)
│   ├── alembic/              # File kịch bản quản lý DB Migrations
│   ├── app/                  # Mã nguồn chính của FastAPI Application
│   │   ├── db/               # Quản lý kết nối Database PostgreSQL (SQLModel/SQLAlchemy)
│   │   ├── knowledge/        # Bộ quy tắc tri thức chuyên gia & khuyến nghị điều trị
│   │   ├── models/           # Định nghĩa bảng dữ liệu (User, DiagnosisHistory, v.v.)
│   │   ├── routers/          # API Routers (Auth, Predict, History, Knowledge)
│   │   ├── services/         # Logic xử lý (Inference Engine ONNX & MinIO Storage Client)
│   │   ├── config.py         # Cấu hình biến môi trường Pydantic Settings
│   │   ├── main.py           # Entry point của ứng dụng FastAPI
│   │   └── security.py       # Quản lý mã hóa mật khẩu & JWT Token Authentication
│   ├── .env.example          # Mẫu biến môi trường cho Backend
│   ├── Dockerfile            # Container build recipe cho Backend FastAPI
│   └── alembic.ini           # Cấu hình Alembic DB Migration
├── crawl/                    # Pipeline Thu thập & Gán nhãn Dữ liệu Tự động / Bán tự động
│   ├── args.py               # Xử lý tham số dòng lệnh cho script crawl
│   ├── crawl_coffee_data.py  # Script thu thập tự động dữ liệu hình ảnh bệnh lá cà phê
│   ├── crawl_rice_data.py    # Script thu thập tự động dữ liệu hình ảnh bệnh lá lúa
│   ├── labeler.py            # Giao diện Streamlit Gán nhãn & Kiểm duyệt (Human-in-the-loop)
│   ├── sam.py                # Mô hình SAM 3 sinh mask phân đoạn tự động (Pseudo-masking)
│   ├── search.py             # Bộ công cụ tìm kiếm hình ảnh qua các Search Engine APIs
│   └── utils.py              # Hàm tiện ích xử lý ảnh thô & hash loại trùng dữ liệu
├── deployment/               # Hạ tầng Triển khai Đám mây & Cục bộ
│   ├── helm/                 # Helm Chart triển khai lên hạ tầng Kubernetes (K3s/GCP)
│   ├── traefik/              # Cấu hình API Gateway, Load Balancing & SSL/TLS Proxy
│   ├── scripts/              # Kịch bản Shell hỗ trợ Healthcheck & Auto Migration
│   ├── .env.example          # Mẫu biến môi trường cho toàn bộ hạ tầng deployment
│   ├── docker-compose.yml    # Docker Compose hạ tầng production/staging
│   └── init-models.ps1       # Script PowerShell tự động tải trọng số mô hình ONNX
├── frontend/                 # Web Application User Interface (Next.js & Tailwind CSS)
│   ├── public/               # Tài nguyên tĩnh (Favicon, Logo, Icons, Images)
│   ├── src/                  # Mã nguồn React / Next.js (App Router)
│   │   ├── app/              # Trang giao diện (Trang chủ, Chẩn đoán, Lịch sử, Tri thức)
│   │   └── components/       # Các UI Component tái sử dụng (Uploader, Result, Card...)
│   ├── .env.example          # Mẫu biến môi trường cho Frontend
│   ├── Dockerfile            # Container build recipe cho Frontend Next.js
│   ├── package.json          # Quản lý dependencies dự án Node.js / React
│   └── tailwind.config.ts    # Cấu hình giao diện Tailwind CSS
├── notebooks/                # Jupyter Notebooks Huấn luyện & Thực nghiệm Mô hình
│   ├── models/               # Notebooks thực nghiệm 5 kiến trúc Phân vùng Thực thể
│   │   ├── mask2former/      # Huấn luyện & Đánh giá mô hình Mask2Former
│   │   ├── mask_rcnn/        # Huấn luyện & Đánh giá mô hình Mask R-CNN (Baseline)
│   │   ├── mobilesam/        # Huấn luyện & Đánh giá mô hình MobileSAM
│   │   ├── rf_detr/          # Huấn luyện & Đánh giá mô hình RF-DETR
│   │   └── yolo26_seg/       # Huấn luyện, Lượng tử hóa (INT8) & Export YOLO26-seg
│   ├── 01_eda.ipynb          # Notebook Phân tích Khám phá Dữ liệu (EDA)
│   └── 02_preprocessing.ipynb# Notebook Tiền xử lý, Augmentation & Đóng gói nhãn COCO
├── scripts/                  # Kịch bản Tiện ích & Công cụ Quản lý Mã nguồn
│   ├── check_masks.py        # Kiểm tra tính hợp lệ của toạ độ mask trong file COCO JSON
│   ├── export_onnx.py        # Export mô hình PyTorch / Ultralytics sang định dạng ONNX
│   ├── export_openapi.py     # Trích xuất OpenAPI Schema (openapi.json) từ FastAPI
│   ├── generate_excalidraw.py# Tự động sinh sơ đồ kiến trúc Excalidraw
│   └── show_masks.py         # Trực quan hóa mask phân đoạn COCO lên hình ảnh
├── src/                      # Thư viện Mã nguồn Python Dùng chung (Shared Python Package)
│   ├── segmentation/         # Module hỗ trợ mô hình phân đoạn (SAM 3 segmenter)
│   └── utils/                # Các hàm tiện ích dùng chung (Config, Helper, Visualize)
├── tests/                    # Bộ Kiểm thử Tự động (Testing Suite)
│   ├── integration/          # Kiểm thử tích hợp end-to-end API Backend & Services
│   ├── load/                 # Kiểm thử tải & hiệu năng hệ thống (Locust load test)
│   ├── test_devops.py        # Kiểm thử hạ tầng Docker & các dịch vụ liên kết
│   ├── test_inference_logic.py # Kiểm thử logic tiền xử lý & suy luận mô hình ONNX
│   ├── test_knowledge_api.py   # Kiểm thử API truy vấn tri thức chuyên gia
│   └── test_knowledge_base.py  # Kiểm thử logic bộ quy tắc tri thức chuyên gia
├── .gitignore                # Khai báo các file/thư mục không commit vào Git
├── .python-version           # Khai báo phiên bản Python mặc định (3.12)
├── alembic.ini               # File cấu hình migration cơ sở dữ liệu Alembic
├── docker-compose.yml        # Multi-container Compose khởi chạy toàn bộ dịch vụ
├── pyproject.toml            # Khai báo phụ thuộc Python & công cụ ruff/pytest (uv package manager)
├── README.md                 # Tài liệu diễn giải cấu trúc mã nguồn (File hiện tại)
└── uv.lock                   # File khóa chính xác phiên bản thư viện Python (Lockfile)
```

---

## 2. Diễn giải Chi tiết từng Module & Thư mục

### 2.1. Backend Service (`backend/`)
Thư mục chứa mã nguồn của hệ thống Backend API được xây dựng bằng **FastAPI**, đảm nhận việc tiếp nhận hình ảnh từ Client, chạy suy luận ONNX Runtime, truy vấn tri thức bệnh học và lưu trữ lịch sử chẩn đoán.

- **`backend/app/main.py`**: Entry point khởi tạo ứng dụng FastAPI, cấu hình CORS, thiết lập middleware và mount các router API.
- **`backend/app/config.py`**: Khai báo và validate biến môi trường (Database URL, Secret Key, MinIO credentials, Model Paths) bằng `pydantic-settings`.
- **`backend/app/security.py`**: Xử lý băm mật khẩu (`passlib`/`bcrypt`), tạo và xác thực JWT token (`python-jose`).
- **`backend/app/db/`**: Quản lý Session kết nối cơ sở dữ liệu PostgreSQL sử dụng `SQLModel` / `SQLAlchemy`.
- **`backend/app/routers/`**:
  - `predict.py`: API xử lý upload ảnh, điều phối mô hình ONNX suy luận vết bệnh lá lúa/cà phê và trả về vùng mask (polygon), bounding box, độ tin cậy và triệu chứng khuyến nghị.
  - `auth.py`: API Đăng ký, Đăng nhập, Trích xuất thông tin người dùng.
  - `history.py`: API lưu vết và truy vấn lịch sử chẩn đoán theo từng tài khoản.
  - `knowledge.py`: API tra cứu chi tiết thông tin bệnh, nguyên nhân và biện pháp điều trị.
- **`backend/app/services/`**:
  - `inference.py`: Service thực thi ONNX Runtime engine. Tiến hành NMS, rescale toạ độ mask polygon, tính diện tích vết bệnh và ghép nhãn lớp.
  - `storage.py`: Client tương tác với MinIO Object Storage để lưu trữ và lấy URL truy cập hình ảnh gốc/kết quả.
- **`backend/app/knowledge/`**:
  - `diseases.json`: Cơ sở dữ liệu tri thức chuyên gia về 8 loại bệnh lá lúa và cà phê (bao gồm nguyên nhân, triệu chứng, biện pháp hóa học và sinh học).
  - `knowledge_base.py`: Trình quản lý và truy vấn bộ quy tắc tri thức.
- **`backend/alembic/` & `alembic.ini`**: Công cụ quản lý cập nhật schema cơ sở dữ liệu tự động.

---

### 2.2. Pipeline Thu thập & Gán nhãn Dữ liệu (`crawl/`)
Mô-đun chịu trách nhiệm thu thập hình ảnh bệnh cây nông nghiệp từ internet và gán nhãn bán tự động áp dụng quy trình **Human-in-the-loop**.

- **`crawl_coffee_data.py` & `crawl_rice_data.py`**: Tự động hóa tìm kiếm hình ảnh qua Bing/Google API và dùng [Crawl4AI](https://github.com/unclecode/crawl4ai) tải ảnh thô về máy local.
- **`search.py`**: Wrapper kết nối tới các dịch vụ tìm kiếm web.
- **`labeler.py`**: Ứng dụng Web gán nhãn bằng Streamlit. Tích hợp Gemma 4 VLM để tự sinh nhãn thô và cho phép chuyên gia hiệu chỉnh lại khung polygon/mask.
- **`sam.py`**: Sử dụng mô hình **SAM 3 (Segment Anything Model)** để biến đổi bounding box thành mask phân đoạn tự động đạt độ chính xác cao.
- **`utils.py` & `args.py`**: Công cụ lọc trùng lặp ảnh dựa trên Perceptual Hash (pHash) và parse tham số cấu hình crawl.

---

### 2.3. Frontend User Interface (`frontend/`)
Ứng dụng giao diện người dùng dựa trên **Next.js 14 (App Router)** và **Tailwind CSS**, cung cấp trải nghiệm hiện đại, mượt mà và tương thích với thiết bị di động.

- **`src/app/`**:
  - `page.tsx`: Trang chính ứng dụng cho phép tải ảnh lá cây, chọn loại cây (Lúa/Cà phê) và xem kết quả chẩn đoán thời gian thực.
  - `layout.tsx`: Layout chung cho toàn bộ trang (Sidebar, Header, Theme Provider).
  - `globals.css`: File định nghĩa style toàn cục, hiệu ứng gradient, animation và CSS custom vars.
- **`src/components/`**:
  - `ImageUploader.tsx`: Component kéo thả tải ảnh với tính năng crop, xem trước.
  - `PredictionResult.tsx`: Component hiển thị hình ảnh đã được vẽ mask phân đoạn vùng bệnh và bảng chỉ số chi tiết.
  - `RecommendationCard.tsx`: Card hiển thị khuyến nghị phòng trừ bệnh từ tri thức chuyên gia.
  - `HistoryList.tsx` & `KnowledgeList.tsx`: Các danh sách tương tác cho lịch sử chẩn đoán và tra cứu bệnh học.
  - `AuthForm.tsx` & `AuthModal.tsx`: Form đăng nhập / đăng ký tài khoản.

---

### 2.4. Notebooks Huấn luyện & Thực nghiệm (`notebooks/`)
Chứa tất cả các Jupyter Notebook ghi lại quá trình EDA, tiền xử lý và huấn luyện thực nghiệm 5 kiến trúc mô hình.

- **`01_eda.ipynb`**: Phân tích số lượng mẫu, sự phân bố kích thước ảnh, độ phân giải, và tỷ lệ bao phủ của mask theo từng lớp bệnh.
- **`02_preprocessing.ipynb`**: Thực hiện chuẩn hóa ảnh, loại bỏ ảnh lỗi, áp dụng kĩ thuật Augmentation và phân chia tập dữ liệu Train/Val/Test theo định dạng COCO.
- **`notebooks/models/`**:
  - `mask_rcnn/`: Huấn luyện mô hình cơ sở Mask R-CNN.
  - `yolo26_seg/`: Huấn luyện YOLO26-seg (Ultralytics), thực hiện Lượng tử hóa mô hình (FP16/INT8) và đóng gói sang file `.onnx`.
  - `mobilesam/`: Thực nghiệm tinh chỉnh (fine-tune) MobileSAM cho tác vụ phân vùng bệnh lá.
  - `rf_detr/`: Thực nghiệm kiến trúc DETR áp dụng cho phân đoạn.
  - `mask2former/`: Huấn luyện Transformer-based segmentation với Mask2Former.

---

### 2.5. Thư viện Mã nguồn Dùng chung (`src/`)
Chứa các module Python được chia sẻ dùng chung giữa quy trình crawl, huấn luyện và API backend.

- **`src/segmentation/sam3_segmenter.py`**: Lớp bao (wrapper) cho mô hình SAM 3 để thực hiện tác vụ segmentation từ gợi ý bounding box.
- **`src/utils/visualize.py`**: Tiện ích vẽ mask phân đoạn đa giác (polygon), gán màu tương ứng từng loại bệnh và ghi nhãn nhị phân.
- **`src/utils/config.py` & `helpers.py`**: Quản lý đường dẫn gốc, thao tác đọc/ghi file JSON/COCO.

---

### 2.6. Thư mục Triển khai Hạ tầng (`deployment/`)
Bao gồm tài nguyên cấu hình triển khai dự án lên môi trường Docker Compose cục bộ và K3s Kubernetes trên GCP.

- **`docker-compose.yml`**: Khởi chạy toàn bộ hệ sinh thái: FastAPI Backend, Next.js Frontend, PostgreSQL, MinIO Storage, Redis, và Traefik Proxy Gateway.
- **`helm/`**: Helm Chart triển khai production lên Kubernetes (Deployment, Service, Ingress, Persistent Volume Claim).
- **`traefik/`**: Cấu hình Traefik Gateway làm Reverse Proxy, tự động cấp phát chứng chỉ SSL/TLS DuckDNS.
- **`init-models.ps1`**: Script PowerShell tự động tải các file trọng số mô hình ONNX từ Google Drive về thư mục `backend/app/models/`.

---

### 2.7. Script Tiện ích (`scripts/`)
Các công cụ tự động hóa công việc quản trị dự án:

- **`export_onnx.py`**: Chuyển đổi mô hình Ultralytics YOLO26-seg sang định dạng ONNX tối ưu hóa cho ONNX Runtime.
- **`export_openapi.py`**: Trích xuất tài liệu API tự động từ ứng dụng FastAPI ra file `openapi.json`.
- **`check_masks.py`**: Kiểm tra tính toàn vẹn dữ liệu mask (phát hiện tọa độ đa giác bị rỗng hoặc nằm ngoài khung ảnh).
- **`show_masks.py`**: Đọc file nhãn COCO và hiển thị trực quan các vùng mask bệnh lên ảnh để nghiệm thu nhãn.
- **`generate_excalidraw.py`**: Tự động sinh sơ đồ kiến trúc Excalidraw phục vụ báo cáo.

---

### 2.8. Bộ Kiểm thử Tự động (`tests/`)
Chứa toàn bộ bộ test case đảm bảo chất lượng hệ thống (Quality Assurance):

- **`test_inference_logic.py`**: Kiểm thử unit test cho pipeline suy luận ONNX (Pre-process -> Model Run -> NMS -> Post-process).
- **`test_knowledge_base.py` & `test_knowledge_api.py`**: Kiểm thử bộ quy tắc tri thức chuyên gia và API tra cứu.
- **`test_devops.py`**: Kiểm thử kết nối hạ tầng (PostgreSQL, MinIO, Redis, FastAPI Healthcheck).
- **`tests/integration/`**: Kiểm thử tích hợp liên dịch vụ (E2E API test).
- **`tests/load/`**: Script kịch bản kiểm thử chịu tải hệ thống bằng **Locust** (`locustfile.py`).

---

### 2.9. Các File Cấu hình Gốc (Root Level Files)

- **`pyproject.toml`**: Định nghĩa cấu hình dự án Python, khai báo dependencies (Backend, Dev, Crawl) tương thích với trình quản lý gói `uv`.
- **`uv.lock`**: File ghi nhớ chính xác phiên bản các thư viện Python để đảm bảo tính nhất quán giữa các môi trường.
- **`docker-compose.yml`**: File cấu hình Docker Compose chính tại root thư mục code cho phép khởi chạy nhanh môi trường dev/staging.
- **`alembic.ini`**: File cấu hình đường dẫn kết nối DB cho Alembic migration.
- **`.python-version`**: Quy định phiên bản Python chuẩn của dự án (`3.12`).

---

## 3. Hướng dẫn Khởi chạy & Sử dụng Mã nguồn

### 3.1. Cài đặt Môi trường Python (sử dụng `uv`)

```bash
# 1. Cài đặt uv (nếu chưa có)
pip install uv

# 2. Cài đặt tất cả phụ thuộc dự án từ pyproject.toml
uv sync --all-groups
```

### 3.2. Tải Trọng số Mô hình ONNX

Chạy script PowerShell để tự động tải trọng số mô hình ONNX đã lượng tử hóa vào đúng vị trí:

```powershell
# Chạy script tải weights
.\deployment\init-models.ps1
```

### 3.3. Khởi chạy Toàn bộ Hệ thống bằng Docker Compose

```bash
# Khởi chạy tất cả dịch vụ (Backend, Frontend, DB, MinIO, Redis, Traefik)
docker compose up -d --build
```

Sau khi khởi chạy:
- **Frontend App**: `http://localhost:3000` (hoặc domain cấu hình)
- **Backend API Swagger Docs**: `http://localhost:8000/docs`
- **MinIO Console**: `http://localhost:9001`

### 3.4. Chạy Kiểm thử (Test Suite)

```bash
# Chạy bộ test tự động với pytest
uv run pytest tests/
```
