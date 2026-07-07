# Template thông tin triển khai Phase 6 - GCP VM, k3s, Helm

## Cách dùng

Tài liệu này là biểu mẫu để nhóm điền thông tin trước khi Xuân Trí setup và deploy Phase 6.

Không điền secret thật trực tiếp vào file nếu file sẽ commit lên repo. Với mật khẩu, token, private key, chỉ ghi tên secret, người giữ secret, và nơi cấu hình secret.

Quyết định kỹ thuật đang đề xuất:

```text
1 GCP VM -> k3s -> Helm -> Traefik/DuckDNS/HTTPS -> frontend/backend/PostgreSQL/MinIO/Redis
```

Không dùng full Kubeflow cho bản demo đầu tiên. Model serving sẽ đi theo hướng ONNX Runtime trong backend pod, model artifact được mount hoặc tải vào `/models`.

## 1. Trạng thái review

| Mục | Giá trị cần điền |
|---|---|
| Ngày cập nhật | `2026-07-07` |
| Người cập nhật | `Nguyễn Hồ Anh Tuấn` |
| Trạng thái | `Ready for review` |
| Người approve cuối | `Nguyễn Hồ Anh Tuấn` |
| Deadline setup infra | `[YYYY-MM-DD HH:mm]` |
| Deadline public demo | `[YYYY-MM-DD HH:mm]` |

## 2. Quyết định cần chốt trước khi làm

| Câu hỏi | Quyết định | Người chốt | Ghi chú |
|---|---|---|---|
| Dùng 1 GCP VM thay vì GKE? | `[Có/Không]` | `[Tên]` | `[Lý do nếu không]` |
| Không dùng full Kubeflow bản demo đầu tiên? | `Có` | `Đàm Tiến Đạt` | `Dùng ONNX Runtime trực tiếp trong backend pod để tối ưu hóa CPU` |
| Server size | `[2vCPU/8GB hoặc 4vCPU/16GB]` | `[Tên]` | `Khuyến nghị 4vCPU/16GB` |
| Registry Docker image | `[GHCR / Google Artifact Registry / Khác]` | `[Tên]` | `[URL registry]` |
| Cách đưa model vào cluster | `[PVC thủ công / build vào image / initContainer tải từ HF-GCS]` | `[Tên]` | `[Lý do chọn]` |
| Ingress controller | `[Traefik / Nginx]` | `[Tên]` | `k3s thường có Traefik sẵn` |
| HTTPS | `[Traefik ACME / cert-manager / HTTP tạm thời]` | `[Tên]` | `[Email Let's Encrypt nếu cần]` |
| MinIO console public? | `Không` | `Tống Thanh Phúc` | `Khuyến nghị không public để bảo mật dữ liệu` |

## 3. Người phụ trách và đầu mối liên hệ

| Phạm vi | Người phụ trách | Việc cần cung cấp | Trạng thái |
|---|---|---|---|
| Infra/K8s/Helm/Ingress/CI-CD | Lê Xuân Trí | VM, k3s, Helm, DuckDNS, deploy pipeline | `Todo` |
| Model artifact và inference | Đàm Tiến Đạt | ONNX, class names, input size, resource inference | `Done` |
| Backend/API/env/migration | Nguyễn Hồ Anh Tuấn | Env production, health probe, migration, API behavior | `Done` |
| DB/MinIO/PVC/backup | Tống Thanh Phúc | PVC size, credential policy, backup need | `Done` |
| Frontend/API URL | Dương Tuấn Anh | API base URL, production build config | `Done` |
| E2E/load test | Nguyễn Hồ Anh Tuấn & Tống Thanh Phúc | Test scenario, sample image, report | `Todo` |

## 4. GCP project và chi phí

| Mục | Giá trị cần điền |
|---|---|
| GCP project ID | `[project-id]` |
| Billing account đã bật? | `[Có/Không]` |
| Budget alert đã tạo? | `[Có/Không]` |
| Budget limit | `[VD: 20 USD]` |
| Region | `[VD: asia-southeast1 / asia-east1 / us-central1]` |
| Zone | `[VD: asia-southeast1-b]` |
| Lý do chọn region/zone | `[Gần VN / rẻ / quota có sẵn / khác]` |
| Người có quyền console GCP | `[Danh sách email]` |
| Người có quyền SSH server | `[Danh sách email/user]` |

## 5. Thông tin VM

| Mục | Giá trị cần điền | Khuyến nghị |
|---|---|---|
| VM name | `[plant-demo-k3s]` | `plant-demo-k3s` |
| Machine type | `[e2-standard-2 / e2-standard-4 / khác]` | `4 vCPU / 16GB RAM nếu đủ ngân sách` |
| OS image | `[Ubuntu 22.04 LTS / Ubuntu 24.04 LTS]` | `Ubuntu LTS` |
| Boot disk size | `[GB]` | `100GB` |
| Boot disk type | `[balanced / SSD]` | `balanced hoặc SSD` |
| Static external IP name | `[Tên static IP]` | `plant-demo-ip` |
| External IP | `[x.x.x.x]` | Điền sau khi tạo |
| Firewall HTTP 80 | `[Mở/Đóng]` | `Mở` |
| Firewall HTTPS 443 | `[Mở/Đóng]` | `Mở` |
| Firewall SSH 22 | `[Mở/Đóng + allowed source]` | `Giới hạn IP nếu có thể` |

## 6. Domain DuckDNS và HTTPS

| Mục | Giá trị cần điền |
|---|---|
| DuckDNS subdomain | `[project-name.duckdns.org]` |
| Static IP đã trỏ vào DuckDNS? | `[Có/Không]` |
| Người giữ DuckDNS token | `[Tên người giữ]` |
| Secret name chứa DuckDNS token | `[VD: duckdns-token]` |
| HTTPS method | `[Traefik ACME / cert-manager / khác]` |
| Email dùng cho Let's Encrypt | `[email]` |
| Public web URL | `https://[project].duckdns.org` |
| Public API URL | `https://[project].duckdns.org/api/v1` |
| Public Swagger URL | `https://[project].duckdns.org/docs` |

## 7. Kubernetes/k3s contract

| Mục | Giá trị cần điền | Khuyến nghị |
|---|---|---|
| Kubernetes distro | `k3s` | `k3s` |
| k3s version | `[stable/latest cụ thể]` | Ghi version sau khi cài |
| Namespace | `plant-disease` | `plant-disease` |
| Helm release name | `plant-disease` | `plant-disease` |
| Helm chart path | `deployment/helm` | `deployment/helm` |
| StorageClass | `local-path` | `local-path` với k3s 1 node |
| Ingress class | `traefik` | `traefik` nếu dùng k3s default |
| kubeconfig lưu ở đâu | `[Server path / GitHub secret / local]` | Không commit kubeconfig |

## 8. Container registry và image naming

| Mục | Giá trị cần điền |
|---|---|
| Registry | `[ghcr.io/<org> hoặc <region>-docker.pkg.dev/<project>/<repo>]` |
| Người tạo registry/repo | `[Tên]` |
| Backend image repository | `[registry]/plant-backend` |
| Frontend image repository | `[registry]/plant-frontend` |
| Tag chính | `[commit SHA]` |
| Tag phụ | `[latest / demo / YYYYMMDD]` |
| Image pull secret name | `[registry-credentials]` |
| Người giữ registry token | `[Tên]` |

## 9. Backend production env

Không điền giá trị secret thật. Với secret, điền tên Kubernetes Secret hoặc GitHub Actions secret.

| Biến môi trường | Giá trị/Secret cần điền | Owner | Ghi chú |
|---|---|---|---|
| `APP_ENV` | `production` | `Nguyễn Hồ Anh Tuấn` | Thiết lập môi trường chạy ứng dụng |
| `MODEL_PATH` | `/models/yolo26_quantized.onnx` | `Đàm Tiến Đạt / Nguyễn Hồ Anh Tuấn` | Đường dẫn đến mô hình YOLO26-seg đã quantized |
| `CLASS_NAMES_PATH` | `/models/class_names.json` | `Đàm Tiến Đạt / Nguyễn Hồ Anh Tuấn` | Đường dẫn file chứa nhãn phân loại |
| `MODEL_INPUT_SIZE` | `640` | `Đàm Tiến Đạt` | Kích thước ảnh đầu vào cho mô hình |
| `MODEL_VERSION` | `yolo26-seg-onnx` | `Đàm Tiến Đạt` | Phiên bản của mô hình |
| `SKIP_DB_INIT` | `false` | `Nguyễn Hồ Anh Tuấn` | Khởi tạo database khi backend startup |
| `SECRET_KEY` | `Secret: [jwt-secret]` | `Nguyễn Hồ Anh Tuấn` | Secret key để mã hóa JWT token |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | `Nguyễn Hồ Anh Tuấn` | Thời gian hết hạn của access token (24 giờ) |
| `POSTGRES_HOST` | `[postgres service name]` | `Tống Thanh Phúc` | Service host của PostgreSQL trong cụm Kubernetes |
| `POSTGRES_PORT` | `5432` | `Tống Thanh Phúc` | Port của PostgreSQL service |
| `POSTGRES_DB` | `plant_disease` | `Tống Thanh Phúc` | Tên database |
| `POSTGRES_USER` | `Secret: [postgres-user]` | `Tống Thanh Phúc` | Username kết nối database |
| `POSTGRES_PASSWORD` | `Secret: [postgres-password]` | `Tống Thanh Phúc` | Password kết nối database |
| `REDIS_URL` | `redis://redis:6379/0` | `Nguyễn Hồ Anh Tuấn` | URL kết nối Redis service trong K8s |
| `MINIO_ENDPOINT` | `minio:9000` | `Tống Thanh Phúc` | Service endpoint của MinIO trong K8s |
| `MINIO_ACCESS_KEY` | `Secret: [minio-access-key]` | `Tống Thanh Phúc` | Access key kết nối MinIO |
| `MINIO_SECRET_KEY` | `Secret: [minio-secret-key]` | `Tống Thanh Phúc` | Secret key kết nối MinIO |
| `MINIO_BUCKET` | `plant-disease-images` | `Tống Thanh Phúc` | Tên bucket lưu trữ ảnh người dùng tải lên |
| `MINIO_SECURE` | `false` | `Tống Thanh Phúc` | Chế độ bảo mật của MinIO |
| `MLFLOW_TRACKING_URI` | `[optional]` | `Đàm Tiến Đạt` | URI tracking MLflow nếu sử dụng (tuỳ chọn) |

## 10. Frontend production env

| Biến/Thông tin | Giá trị cần điền | Owner | Ghi chú |
|---|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | `https://[project].duckdns.org/api/v1` | `Dương Tuấn Anh` | Build-time env cho Frontend Next.js |
| Frontend port trong container | `3000` | `Dương Tuấn Anh` | Port exposure trong container |
| Frontend health path nếu có | `/` | `Dương Tuấn Anh` | Path kiểm tra trạng thái hoạt động của frontend |
| Cần rebuild khi đổi API URL? | `Có` | `Dương Tuấn Anh` | Next.js public env cần rebuild khi thay đổi URL build-time |

## 11. Model artifact do Đàm Tiến Đạt cung cấp

| Mục | Giá trị cần điền | Bắt buộc? |
|---|---|---|
| File ONNX cuối | `yolo26_quantized.onnx` | Có |
| Đường dẫn local mong muốn | `/models/yolo26_quantized.onnx` | Có |
| `class_names.json` | `Có (models/class_names.json)` | Có |
| Input size | `640` | Có |
| Preprocessing | `Resize (640x640), normalize (/ 255.0), transpose sang NCHW float32` | Có |
| Output format | `output0: [1, 300, 38] (4 bbox, 8 classes, 26 masks); output1: [1, 32, 160, 160] (32 prototype masks)` | Có |
| Model version | `yolo26-seg-onnx` | Có |
| Source artifact | `models/yolo26_quantized.onnx` | Có |
| Artifact private? | `Không` | Có |
| Token/secret name nếu private | `[model-download-token]` | Nếu private |
| Expected CPU RAM | `~40MB cho ONNX session loading (Khuyến nghị cấp 2GB cho pod)` | Có |
| Expected latency CPU | `~1500 ms/image` | Nên có |
| Sample image để test | `data/raw/` hoặc bất kỳ ảnh lá cà phê/lúa | Có |
| Expected sample output | `Nhãn bệnh (8 lớp: Healthy, BrownSpot, Hispa, LeafBlast, LeafMiner, PowderyMildew, Rust, AlgalLeafSpot) kèm bounding box & segmentation mask` | Nên có |

## 12. Cách đưa model vào cluster

Chọn đúng một phương án cho bản demo đầu tiên.

| Phương án | Chọn? | Ai làm | Ghi chú |
|---|---|---|---|
| A. Copy model thủ công vào PVC trên server | `Không` | `Đàm Tiến Đạt` | Nhanh nhất cho demo |
| B. Build model vào backend image | `Có` | `Đàm Tiến Đạt` | Cấu hình tự động copy vào backend image (`COPY models /models`) |
| C. InitContainer tải model từ Hugging Face/GCS vào PVC | `Không` | `Đàm Tiến Đạt` | Sạch hơn cho CI/CD |

Nếu chọn A:

| Mục | Giá trị cần điền |
|---|---|
| PVC name | `N/A` |
| Mount path | `N/A` |
| Người upload model lên server | `N/A` |
| Lệnh/Runbook upload | `N/A` |

Nếu chọn C:

| Mục | Giá trị cần điền |
|---|---|
| Artifact URL | `N/A` |
| Secret/token name | `N/A` |
| Init image | `N/A` |
| Checksum file | `N/A` |

## 13. Database, MinIO, Redis và persistence

| Service | Dạng deploy | PVC size | Có backup? | Public? | Owner |
|---|---|---|---|---|---|
| PostgreSQL | `StatefulSet/Chart dependency` | `20Gi` | `[Có/Không]` | `Không` | `Tống Thanh Phúc` |
| MinIO | `StatefulSet/Chart dependency` | `30Gi` | `[Có/Không]` | `Không` | `Tống Thanh Phúc` |
| Redis | `Deployment/StatefulSet` | `[Không cần/size]` | `Không` | `Không` | `Nguyễn Hồ Anh Tuấn` |
| Model PVC | `PVC` | `10Gi` | `Không` | `Không` | `Đàm Tiến Đạt` |

Thông tin cần chốt thêm:

- Migration Alembic chạy tự động khi backend start? `Có`
- Có cần seed dữ liệu demo không? `[Có/Không]`
- Có cần backup trước buổi demo không? `[Có/Không]`
- Nếu backup, ai chạy và lưu ở đâu? `Tống Thanh Phúc`

## 14. Ingress routes

| Route | Service đích | Public? | Auth/protection | Ghi chú |
|---|---|---|---|---|
| `/` | `frontend` | Có | Không | Web app (Owner: `Dương Tuấn Anh`) |
| `/api/v1` | `backend` | Có | App auth | API (Owner: `Nguyễn Hồ Anh Tuấn`) |
| `/docs` | `backend` | `Có` | `Không` | Swagger (Owner: `Nguyễn Hồ Anh Tuấn`) |
| `/redoc` | `backend` | `[Có/Không]` | `[Không/IP allowlist]` | ReDoc (Owner: `Nguyễn Hồ Anh Tuấn`) |
| `/minio` hoặc MinIO console | `minio-console` | `Không` | `[Basic/IP allowlist]` | Chỉ public nếu thật cần (Owner: `Tống Thanh Phúc`) |
| `/mlflow` | `mlflow` | `[Không/Optional]` | `[Basic/IP allowlist]` | Chỉ nếu deploy MLflow (Owner: `Đàm Tiến Đạt`) |

## 15. GitHub Actions secrets cần cấu hình

Không ghi giá trị thật ở đây.

| Secret name | Dùng cho | Người cung cấp | Đã cấu hình? |
|---|---|---|---|
| `REGISTRY_USERNAME` | Push/pull image | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `REGISTRY_TOKEN` | Push/pull image | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `GCP_VM_HOST` | SSH deploy | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `GCP_VM_USER` | SSH deploy | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `GCP_VM_SSH_KEY` | SSH deploy | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `POSTGRES_PASSWORD` | Helm secret | `Tống Thanh Phúc` | `Chưa (Chờ Phase 6)` |
| `MINIO_SECRET_KEY` | Helm secret | `Tống Thanh Phúc` | `Chưa (Chờ Phase 6)` |
| `JWT_SECRET_KEY` | Backend secret | `Nguyễn Hồ Anh Tuấn` | `Chưa (Chờ Phase 6)` |
| `DUCKDNS_TOKEN` | HTTPS/DNS automation nếu cần | `Lê Xuân Trí` | `Chưa (Chờ Phase 6)` |
| `MODEL_DOWNLOAD_TOKEN` | Tải model private nếu cần | `Đàm Tiến Đạt` | `N/A (Build thẳng vào image)` |

## 16. Helm values template cần điền

```yaml
global:
  namespace: plant-disease
  domain: "[project].duckdns.org"

images:
  backend:
    repository: "[registry]/plant-backend"
    tag: "[commit-sha]"
  frontend:
    repository: "[registry]/plant-frontend"
    tag: "[commit-sha]"
  imagePullSecret: "[registry-credentials]"

frontend:
  env:
    NEXT_PUBLIC_API_BASE_URL: "https://[project].duckdns.org/api/v1"

backend:
  env:
    APP_ENV: "production"
    MODEL_PATH: "/models/yolo26_quantized.onnx"
    CLASS_NAMES_PATH: "/models/class_names.json"
    MODEL_INPUT_SIZE: "640"
    MODEL_VERSION: "yolo26-seg-onnx"
  resources:
    requests:
      cpu: "500m"
      memory: "2Gi"
    limits:
      cpu: "2"
      memory: "6Gi"

postgres:
  persistence:
    size: "20Gi"

minio:
  persistence:
    size: "30Gi"

model:
  persistence:
    size: "10Gi"
  deliveryMode: "image"
```

## 17. CI/CD pipeline cần xác nhận

| Job | Có cần? | Điều kiện pass | Owner |
|---|---|---|---|
| `lint-and-test` | Có | Python tests pass, frontend build/test nếu có | `Lê Xuân Trí / Nguyễn Hồ Anh Tuấn / Dương Tuấn Anh` |
| `build-backend` | Có | Backend image build được | `Lê Xuân Trí` |
| `build-frontend` | Có | Frontend image build được | `Lê Xuân Trí` |
| `push-images` | Có | Image có tag commit SHA trên registry | `Lê Xuân Trí` |
| `deploy` | Có | `helm upgrade --install` thành công | `Lê Xuân Trí` |
| `smoke-test` | Có | Health, knowledge API, web URL pass | `Nguyễn Hồ Anh Tuấn` |
| `predict-e2e` | Khi model sẵn sàng | Upload ảnh -> nhận prediction | `Nguyễn Hồ Anh Tuấn & Đàm Tiến Đạt` |

## 18. Test evidence cần có trước khi demo

| Evidence | Command hoặc URL | Người chạy | Kết quả | Link/log |
|---|---|---|---|---|
| Pods running | `kubectl -n plant-disease get pods` | `Lê Xuân Trí` | `[Pass/Fail]` | `[Log]` |
| Ingress ready | `kubectl -n plant-disease get ingress` | `Lê Xuân Trí` | `[Pass/Fail]` | `[Log]` |
| Web public URL | `https://[project].duckdns.org` | `Dương Tuấn Anh` | `[Pass/Fail]` | `[Screenshot/log]` |
| API health | `curl -f https://[project].duckdns.org/health` | `Nguyễn Hồ Anh Tuấn` | `[Pass/Fail]` | `[Log]` |
| Knowledge API | `curl -f https://[project].duckdns.org/api/v1/knowledge` | `Lê Xuân Trí / Nguyễn Hồ Anh Tuấn` | `[Pass/Fail]` | `[Log]` |
| Auth flow | Register/login | `Nguyễn Hồ Anh Tuấn` | `[Pass/Fail]` | `[Log]` |
| Predict flow | Upload sample leaf | `Nguyễn Hồ Anh Tuấn / Đàm Tiến Đạt` | `[Pass/Fail]` | `[Log]` |
| History flow | Login -> predict -> history | `Nguyễn Hồ Anh Tuấn` | `[Pass/Fail]` | `[Log]` |
| Restart safety | Restart backend pod | `Lê Xuân Trí / Nguyễn Hồ Anh Tuấn` | `[Pass/Fail]` | `[Log]` |
| Load smoke | `[Tool/command]` | `Nguyễn Hồ Anh Tuấn & Tống Thanh Phúc` | `[Pass/Fail]` | `[Report]` |

## 19. Runbook cần chuẩn bị

| Runbook | Có chưa? | Path/Link | Owner |
|---|---|---|---|
| Tạo VM GCP | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |
| Cài k3s | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |
| Cấu hình DuckDNS/HTTPS | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |
| Deploy bằng Helm | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |
| Upload/tải model | `[Có/Không]` | `[path]` | `Đàm Tiến Đạt` |
| Backup DB/MinIO | `[Có/Không]` | `[path]` | `Tống Thanh Phúc` |
| Rollback Helm release | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |
| Tắt server để tránh tốn phí | `[Có/Không]` | `[path]` | `Lê Xuân Trí` |

## 20. Blocker hiện tại

| Blocker | Ảnh hưởng | Người xử lý | Deadline | Trạng thái |
|---|---|---|---|---|
| `Không có blocker từ Phase 5` | `N/A` | `N/A` | `N/A` | `Closed` |

## 21. Checklist approve trước khi Xuân Trí setup

- [ ] Team chấp nhận dùng 1 GCP VM + k3s thay vì GKE.
- [ ] Team chấp nhận không dùng full Kubeflow trong bản demo đầu tiên.
- [ ] Đã chốt machine type và budget.
- [ ] Đã chốt domain DuckDNS.
- [ ] Đã chốt registry và image naming.
- [ ] Đã chốt cách đưa model vào cluster.
- [x] Đã có hoặc có deadline rõ cho `yolo26_quantized.onnx`. (Đã hoàn thành ở Phase 5)
- [x] Đã có hoặc có deadline rõ cho `class_names.json`. (Đã hoàn thành ở Phase 5)
- [x] Backend owner đã xác nhận env production. (Nguyễn Hồ Anh Tuấn đã xác nhận)
- [x] Frontend owner đã xác nhận API base URL. (Dương Tuấn Anh đã xác nhận)
- [x] DB/storage owner đã xác nhận PVC size. (Tống Thanh Phúc đã xác nhận)
- [ ] Người giữ secret đã sẵn sàng cung cấp qua kênh an toàn.
- [ ] Có người chịu trách nhiệm E2E verification. (Nguyễn Hồ Anh Tuấn chịu trách nhiệm)

## 22. Ghi chú review

Điền các ý kiến review của team ở đây:

```text
[Nguyễn Hồ Anh Tuấn - 2026-07-07]
- Ý kiến: Kế hoạch Phase 5 đã được cập nhật đầy đủ và chuẩn xác dựa trên WEB_PLAN.md. Sẵn sàng cho việc review và chuyển giao sang Phase 6.
- Quyết định: Cần thống nhất các lựa chọn hạ tầng trong Phase 6 (VM size, domain DuckDNS, Registry) trước khi tiến hành triển khai.
- Việc cần làm tiếp: Trí tiến hành setup infrastructure sau khi chốt các lựa chọn của Phase 6.
```
