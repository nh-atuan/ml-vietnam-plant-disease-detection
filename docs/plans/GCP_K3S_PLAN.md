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
| Ngày cập nhật | `[YYYY-MM-DD]` |
| Người cập nhật | `[Tên người cập nhật]` |
| Trạng thái | `[Draft / Ready for setup / Blocked / Approved]` |
| Người approve cuối | `[Tên người approve]` |
| Deadline setup infra | `[YYYY-MM-DD HH:mm]` |
| Deadline public demo | `[YYYY-MM-DD HH:mm]` |

## 2. Quyết định cần chốt trước khi làm

| Câu hỏi | Quyết định | Người chốt | Ghi chú |
|---|---|---|---|
| Dùng 1 GCP VM thay vì GKE? | `[Có/Không]` | `[Tên]` | `[Lý do nếu không]` |
| Không dùng full Kubeflow bản demo đầu tiên? | `[Có/Không]` | `[Tên]` | `[Nếu cần KServe/Kubeflow, ghi phạm vi]` |
| Server size | `[2vCPU/8GB hoặc 4vCPU/16GB]` | `[Tên]` | `Khuyến nghị 4vCPU/16GB` |
| Registry Docker image | `[GHCR / Google Artifact Registry / Khác]` | `[Tên]` | `[URL registry]` |
| Cách đưa model vào cluster | `[PVC thủ công / build vào image / initContainer tải từ HF-GCS]` | `[Tên]` | `[Lý do chọn]` |
| Ingress controller | `[Traefik / Nginx]` | `[Tên]` | `k3s thường có Traefik sẵn` |
| HTTPS | `[Traefik ACME / cert-manager / HTTP tạm thời]` | `[Tên]` | `[Email Let's Encrypt nếu cần]` |
| MinIO console public? | `[Không / Có, protected]` | `[Tên]` | `Khuyến nghị không public` |

## 3. Người phụ trách và đầu mối liên hệ

| Phạm vi | Người phụ trách | Việc cần cung cấp | Trạng thái |
|---|---|---|---|
| Infra/K8s/Helm/Ingress/CI-CD | Lê Xuân Trí | VM, k3s, Helm, DuckDNS, deploy pipeline | `[Todo/Doing/Done]` |
| Model artifact và inference | Đàm Tiến Đạt | ONNX, class names, input size, resource inference | `[Todo/Doing/Done]` |
| Backend/API/env/migration | `[Tên backend owner]` | Env production, health probe, migration, API behavior | `[Todo/Doing/Done]` |
| DB/MinIO/PVC/backup | `[Tên DB/storage owner]` | PVC size, credential policy, backup need | `[Todo/Doing/Done]` |
| Frontend/API URL | `[Tên frontend owner]` | API base URL, production build config | `[Todo/Doing/Done]` |
| E2E/load test | `[Tên QC owner]` | Test scenario, sample image, report | `[Todo/Doing/Done]` |

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
| Kubernetes distro | `[k3s]` | `k3s` |
| k3s version | `[stable/latest cụ thể]` | Ghi version sau khi cài |
| Namespace | `[plant-disease]` | `plant-disease` |
| Helm release name | `[plant-disease]` | `plant-disease` |
| Helm chart path | `[deployment/helm]` | `deployment/helm` |
| StorageClass | `[local-path / khác]` | `local-path` với k3s 1 node |
| Ingress class | `[traefik / nginx]` | `traefik` nếu dùng k3s default |
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
| `APP_ENV` | `production` | Backend |  |
| `MODEL_PATH` | `/models/yolo26_quantized.onnx` | Model/Backend |  |
| `CLASS_NAMES_PATH` | `/models/class_names.json` | Model/Backend |  |
| `MODEL_INPUT_SIZE` | `[640 hoặc giá trị khác]` | Model |  |
| `MODEL_VERSION` | `[yolo26-seg-onnx hoặc version cụ thể]` | Model |  |
| `SKIP_DB_INIT` | `[false/true]` | Backend | Chốt migration strategy |
| `SECRET_KEY` | `Secret: [jwt-secret]` | Backend | Không commit giá trị |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `[1440 hoặc khác]` | Backend |  |
| `POSTGRES_HOST` | `[postgres service name]` | DB |  |
| `POSTGRES_PORT` | `5432` | DB |  |
| `POSTGRES_DB` | `[plant_disease]` | DB |  |
| `POSTGRES_USER` | `Secret: [postgres-user]` | DB |  |
| `POSTGRES_PASSWORD` | `Secret: [postgres-password]` | DB | Không commit giá trị |
| `REDIS_URL` | `[redis://redis:6379/0]` | Backend |  |
| `MINIO_ENDPOINT` | `[minio:9000]` | Storage | Internal service |
| `MINIO_ACCESS_KEY` | `Secret: [minio-access-key]` | Storage | Không commit giá trị |
| `MINIO_SECRET_KEY` | `Secret: [minio-secret-key]` | Storage | Không commit giá trị |
| `MINIO_BUCKET` | `[plant-disease-images]` | Storage |  |
| `MINIO_SECURE` | `[false]` | Storage | Internal MinIO thường false |
| `MLFLOW_TRACKING_URI` | `[optional]` | Model | Chỉ điền nếu deploy MLflow |

## 10. Frontend production env

| Biến/Thông tin | Giá trị cần điền | Owner | Ghi chú |
|---|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | `https://[project].duckdns.org/api/v1` | Frontend | Build-time env |
| Frontend port trong container | `[3000]` | Frontend |  |
| Frontend health path nếu có | `[/ hoặc custom]` | Frontend |  |
| Cần rebuild khi đổi API URL? | `[Có/Không]` | Frontend | Next public env thường cần rebuild |

## 11. Model artifact do Đàm Tiến Đạt cung cấp

| Mục | Giá trị cần điền | Bắt buộc? |
|---|---|---|
| File ONNX cuối | `[Tên file]` | Có |
| Đường dẫn local mong muốn | `/models/yolo26_quantized.onnx` | Có |
| `class_names.json` | `[Có/Không + nguồn]` | Có |
| Input size | `[VD: 640]` | Có |
| Preprocessing | `[resize/letterbox/normalize/channel order]` | Có |
| Output format | `[classification/top-k/segmentation output details]` | Có |
| Model version | `[version/tag/date]` | Có |
| Source artifact | `[Hugging Face URL / GCS path / upload thủ công]` | Có |
| Artifact private? | `[Có/Không]` | Có |
| Token/secret name nếu private | `[model-download-token]` | Nếu private |
| Expected CPU RAM | `[VD: 2GB/4GB/6GB]` | Có |
| Expected latency CPU | `[ms/image]` | Nên có |
| Sample image để test | `[path hoặc URL]` | Có |
| Expected sample output | `[label/confidence gần đúng]` | Nên có |

## 12. Cách đưa model vào cluster

Chọn đúng một phương án cho bản demo đầu tiên.

| Phương án | Chọn? | Ai làm | Ghi chú |
|---|---|---|---|
| A. Copy model thủ công vào PVC trên server | `[Có/Không]` | `[Tên]` | Nhanh nhất cho demo |
| B. Build model vào backend image | `[Có/Không]` | `[Tên]` | Image nặng hơn |
| C. InitContainer tải model từ Hugging Face/GCS vào PVC | `[Có/Không]` | `[Tên]` | Sạch hơn cho CI/CD |

Nếu chọn A:

| Mục | Giá trị cần điền |
|---|---|
| PVC name | `[model-pvc]` |
| Mount path | `/models` |
| Người upload model lên server | `[Tên]` |
| Lệnh/Runbook upload | `[Điền sau]` |

Nếu chọn C:

| Mục | Giá trị cần điền |
|---|---|
| Artifact URL | `[hf/gcs url]` |
| Secret/token name | `[model-download-token]` |
| Init image | `[curl/wget/gcloud/custom]` |
| Checksum file | `[sha256 nếu có]` |

## 13. Database, MinIO, Redis và persistence

| Service | Dạng deploy | PVC size | Có backup? | Public? | Owner |
|---|---|---|---|---|---|
| PostgreSQL | `[StatefulSet/Chart dependency]` | `[20Gi]` | `[Có/Không]` | `Không` | `[Tên]` |
| MinIO | `[StatefulSet/Chart dependency]` | `[30Gi]` | `[Có/Không]` | `[Không/Console protected]` | `[Tên]` |
| Redis | `[Deployment/StatefulSet]` | `[Không cần/size]` | `[Không]` | `Không` | `[Tên]` |
| Model PVC | `[PVC]` | `[10Gi hoặc theo model]` | `[Có/Không]` | `Không` | `[Tên]` |

Thông tin cần chốt thêm:

- Migration Alembic chạy tự động khi backend start? `[Có/Không]`
- Có cần seed dữ liệu demo không? `[Có/Không]`
- Có cần backup trước buổi demo không? `[Có/Không]`
- Nếu backup, ai chạy và lưu ở đâu? `[Tên + vị trí]`

## 14. Ingress routes

| Route | Service đích | Public? | Auth/protection | Ghi chú |
|---|---|---|---|---|
| `/` | `frontend` | Có | Không | Web app |
| `/api/v1` | `backend` | Có | App auth | API |
| `/docs` | `backend` | `[Có/Không]` | `[Không/IP allowlist]` | Swagger |
| `/redoc` | `backend` | `[Có/Không]` | `[Không/IP allowlist]` | ReDoc |
| `/minio` hoặc MinIO console | `minio-console` | `[Không khuyến nghị]` | `[Basic/IP allowlist]` | Chỉ public nếu thật cần |
| `/mlflow` | `mlflow` | `[Không/Optional]` | `[Basic/IP allowlist]` | Chỉ nếu deploy MLflow |

## 15. GitHub Actions secrets cần cấu hình

Không ghi giá trị thật ở đây.

| Secret name | Dùng cho | Người cung cấp | Đã cấu hình? |
|---|---|---|---|
| `REGISTRY_USERNAME` | Push/pull image | `[Tên]` | `[Có/Không]` |
| `REGISTRY_TOKEN` | Push/pull image | `[Tên]` | `[Có/Không]` |
| `GCP_VM_HOST` | SSH deploy | `[Tên]` | `[Có/Không]` |
| `GCP_VM_USER` | SSH deploy | `[Tên]` | `[Có/Không]` |
| `GCP_VM_SSH_KEY` | SSH deploy | `[Tên]` | `[Có/Không]` |
| `POSTGRES_PASSWORD` | Helm secret | `[Tên]` | `[Có/Không]` |
| `MINIO_SECRET_KEY` | Helm secret | `[Tên]` | `[Có/Không]` |
| `JWT_SECRET_KEY` | Backend secret | `[Tên]` | `[Có/Không]` |
| `DUCKDNS_TOKEN` | HTTPS/DNS automation nếu cần | `[Tên]` | `[Có/Không]` |
| `MODEL_DOWNLOAD_TOKEN` | Tải model private nếu cần | `[Tên]` | `[Có/Không]` |

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
    MODEL_INPUT_SIZE: "[640]"
    MODEL_VERSION: "[yolo26-seg-onnx]"
  resources:
    requests:
      cpu: "[500m]"
      memory: "[2Gi]"
    limits:
      cpu: "[2]"
      memory: "[6Gi]"

postgres:
  persistence:
    size: "[20Gi]"

minio:
  persistence:
    size: "[30Gi]"

model:
  persistence:
    size: "[10Gi]"
  deliveryMode: "[manual-pvc | image | init-container]"
```

## 17. CI/CD pipeline cần xác nhận

| Job | Có cần? | Điều kiện pass | Owner |
|---|---|---|---|
| `lint-and-test` | Có | Python tests pass, frontend build/test nếu có | `[Tên]` |
| `build-backend` | Có | Backend image build được | `[Tên]` |
| `build-frontend` | Có | Frontend image build được | `[Tên]` |
| `push-images` | Có | Image có tag commit SHA trên registry | `[Tên]` |
| `deploy` | Có | `helm upgrade --install` thành công | `[Tên]` |
| `smoke-test` | Có | Health, knowledge API, web URL pass | `[Tên]` |
| `predict-e2e` | Khi model sẵn sàng | Upload ảnh -> nhận prediction | `[Tên]` |

## 18. Test evidence cần có trước khi demo

| Evidence | Command hoặc URL | Người chạy | Kết quả | Link/log |
|---|---|---|---|---|
| Pods running | `kubectl -n plant-disease get pods` | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Ingress ready | `kubectl -n plant-disease get ingress` | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Web public URL | `https://[project].duckdns.org` | `[Tên]` | `[Pass/Fail]` | `[Screenshot/log]` |
| API health | `curl -f https://[project].duckdns.org/health` | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Knowledge API | `curl -f https://[project].duckdns.org/api/v1/knowledge` | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Auth flow | Register/login | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Predict flow | Upload sample leaf | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| History flow | Login -> predict -> history | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Restart safety | Restart backend pod | `[Tên]` | `[Pass/Fail]` | `[Log]` |
| Load smoke | `[Tool/command]` | `[Tên]` | `[Pass/Fail]` | `[Report]` |

## 19. Runbook cần chuẩn bị

| Runbook | Có chưa? | Path/Link | Owner |
|---|---|---|---|
| Tạo VM GCP | `[Có/Không]` | `[path]` | `[Tên]` |
| Cài k3s | `[Có/Không]` | `[path]` | `[Tên]` |
| Cấu hình DuckDNS/HTTPS | `[Có/Không]` | `[path]` | `[Tên]` |
| Deploy bằng Helm | `[Có/Không]` | `[path]` | `[Tên]` |
| Upload/tải model | `[Có/Không]` | `[path]` | `[Tên]` |
| Backup DB/MinIO | `[Có/Không]` | `[path]` | `[Tên]` |
| Rollback Helm release | `[Có/Không]` | `[path]` | `[Tên]` |
| Tắt server để tránh tốn phí | `[Có/Không]` | `[path]` | `[Tên]` |

## 20. Blocker hiện tại

| Blocker | Ảnh hưởng | Người xử lý | Deadline | Trạng thái |
|---|---|---|---|---|
| `[VD: chưa có yolo26_quantized.onnx]` | `[Predict chưa chạy thật]` | `[Tên]` | `[YYYY-MM-DD]` | `[Open]` |
| `[VD: chưa có domain DuckDNS]` | `[Chưa public demo]` | `[Tên]` | `[YYYY-MM-DD]` | `[Open]` |
| `[VD: chưa có registry token]` | `[CI/CD chưa push image]` | `[Tên]` | `[YYYY-MM-DD]` | `[Open]` |

## 21. Checklist approve trước khi Xuân Trí setup

- [ ] Team chấp nhận dùng 1 GCP VM + k3s thay vì GKE.
- [ ] Team chấp nhận không dùng full Kubeflow trong bản demo đầu tiên.
- [ ] Đã chốt machine type và budget.
- [ ] Đã chốt domain DuckDNS.
- [ ] Đã chốt registry và image naming.
- [ ] Đã chốt cách đưa model vào cluster.
- [ ] Đã có hoặc có deadline rõ cho `yolo26_quantized.onnx`.
- [ ] Đã có hoặc có deadline rõ cho `class_names.json`.
- [ ] Backend owner đã xác nhận env production.
- [ ] Frontend owner đã xác nhận API base URL.
- [ ] DB/storage owner đã xác nhận PVC size.
- [ ] Người giữ secret đã sẵn sàng cung cấp qua kênh an toàn.
- [ ] Có người chịu trách nhiệm E2E verification.

## 22. Ghi chú review

Điền các ý kiến review của team ở đây:

```text
[Tên - ngày giờ]
- Ý kiến:
- Quyết định:
- Việc cần làm tiếp:
```
