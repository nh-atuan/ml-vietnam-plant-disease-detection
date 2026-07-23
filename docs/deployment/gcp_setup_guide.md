# Hướng dẫn chi tiết thiết lập GCP Server & k3s (Thống nhất theo GCP_K3S_PLAN.md)

Tài liệu này cung cấp hướng dẫn chi tiết từng bước để thiết lập máy chủ GCP, cài đặt k3s, cấu hình DuckDNS và deploy ứng dụng. Toàn bộ tên gọi, thông số, IP mẫu và cấu hình trong hướng dẫn này được đồng bộ và thống nhất 100% với tệp kế hoạch [GCP_K3S_PLAN.md](GCP_K3S_PLAN.md).

---

## Kiến trúc hệ thống thống nhất

* **GCP Project ID**: `plant-disease-demo`
* **GCP Region/Zone**: `asia-southeast1` / `asia-southeast1-b` (Singapore)
* **VM Instance Name**: `plant-demo-k3s`
* **Static External IP**: `35.240.231.12` (Tên IP: `plant-demo-ip`)
* **DuckDNS Subdomain**: `plant-disease-demo` (Domain: `plant-disease-demo.duckdns.org`)
* **Kubernetes Namespace**: `plant-disease`
* **Helm Release Name**: `plant-disease`
* **Registry**: `ghcr.io/nh-atuan/ml-vietnam-plant-disease-detection`

---

## Bước 1: Tạo GCP Project và Kích hoạt Billing

1. **Truy cập GCP Console**: Đăng nhập vào [Google Cloud Console](https://console.cloud.google.com/).
2. **Tạo Project**:
   - Ở menu chọn project (góc trên bên trái), chọn **New Project**.
   - Điền **Project name**: `plant-disease-demo` (hoặc tên có chứa ID này nếu trùng lặp).
   - Nhấp **Create**.
3. **Kích hoạt Billing**:
   - Vào menu **Billing** và đảm bảo Project đã liên kết với một Billing Account hoạt động.
4. **Cấu hình Cảnh báo ngân sách (Budget Alert)**:
   - Trong **Billing**, vào mục **Budgets & alerts** -> **Create Budget**.
   - Đặt giới hạn ngân sách là `20 USD`.
   - Chọn nhận email cảnh báo khi chi tiêu đạt `50%`, `90%` và `100%`.

---

## Bước 2: Tạo máy ảo Compute Engine VM

1. Truy cập **Compute Engine** -> **VM instances** -> **Create Instance**.
2. Nhập chính xác các thông tin cấu hình sau:
   * **Name**: `plant-demo-k3s`
   * **Region**: `asia-southeast1` (Singapore)
   * **Zone**: `asia-southeast1-b`
   * **Machine configuration**:
     * **Series**: `E2`
     * **Machine type**: **`e2-standard-4` (4 vCPUs, 16 GB RAM)** (theo đúng khuyến nghị của kế hoạch để chạy ổn định model ONNX, DB, MinIO và web app).
   * **Boot disk**: Nhấp **Change**:
     * **Operating System**: `Ubuntu`
     * **Version**: `Ubuntu 22.04 LTS`
     * **Boot disk type**: `Balanced persistent disk`
     * **Size**: `100 GB`
   * **Firewall**: Tích chọn:
     * `Allow HTTP traffic`
     * `Allow HTTPS traffic`
3. Nhấp **Create** để khởi tạo máy ảo.

---

## Bước 3: Đặt địa chỉ IP ngoại vi tĩnh (Static External IP)

1. Gõ lên thanh tìm kiếm GCP: **VPC network** -> **IP addresses**.
2. Tìm địa chỉ IP ngoại vi của VM `plant-demo-k3s` (đang hiển thị ở trạng thái `Ephemeral`).
3. Chọn dấu 3 chấm bên phải dòng đó -> chọn **Promote to static IP address**.
4. Đặt tên gợi nhớ: `plant-demo-ip`.
5. Sau khi lưu, hệ thống sẽ cố định IP cho bạn (Ví dụ IP tĩnh được cấp là: `35.240.231.12`).

---

## Bước 4: Tạo tên miền DuckDNS

1. Truy cập [DuckDNS](https://www.duckdns.org/) và đăng nhập.
2. Tại phần **subdomains**, gõ chính xác tên miền: `plant-disease-demo` rồi nhấn **add domain**.
3. Sau khi thêm thành công, điền IP tĩnh của bạn (ví dụ: `35.240.231.12`) vào ô **ip** và nhấn **update ip**.
4. Lưu lại **DuckDNS Token** của bạn từ trang chủ DuckDNS để cấu hình cho script tự động cập nhật IP.

---

## Bước 5: Cấu hình khóa SSH kết nối máy ảo VM

Bạn cần sinh cặp khóa SSH ở máy cá nhân (Local) để đăng nhập và giúp GitHub Actions deploy tự động.

### 5.1. Tạo SSH Key ở máy cá nhân (Local)
Mở Terminal ở máy cá nhân của bạn và chạy:
```bash
# Tạo thư mục SSH nếu chưa có
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Tạo cặp khóa SSH Ed25519
ssh-keygen -t ed25519 -C "k3s-deploy" -f ~/.ssh/k3s_deploy_key
# Bấm Enter để bỏ qua Passphrase (bắt buộc để CI/CD chạy tự động không bị kẹt)
```

### 5.2. Đưa Khóa công khai lên GCP VM
1. Truy cập GCP Console -> **Compute Engine** -> **Metadata**.
2. Chọn tab **SSH Keys** -> Nhấp **Edit** -> Nhấp **Add item**.
3. Mở file `~/.ssh/k3s_deploy_key.pub` trên máy cá nhân bằng editor hoặc chạy `cat ~/.ssh/k3s_deploy_key.pub`, copy toàn bộ nội dung và dán vào ô nhập liệu trên GCP Console.
4. Bấm **Save**. GCP sẽ tự động tạo user trên VM tương ứng với phần tên trước ký tự `@` trong file public key của bạn (Ví dụ user là `pearspringmind`).

---

## Bước 6: Cài đặt k3s, Helm và cert-manager trên GCP VM

### 6.1. Đăng nhập vào VM qua SSH
Chạy lệnh sau trên máy cá nhân (Local) để SSH vào VM:
```bash
ssh -i ~/.ssh/k3s_deploy_key pearspringmind@35.240.231.12
# Thay 'pearspringmind' bằng username của bạn trên VM và '35.240.231.12' bằng IP tĩnh thực tế của VM
```

### 6.2. Chạy Script cài đặt hạ tầng k3s
Khi đã đăng nhập thành công vào VM, hãy thực hiện clone repository và khởi tạo k3s:
```bash
# Clone dự án về thư mục ứng dụng trên máy chủ VM
git clone https://github.com/nh-atuan/ml-vietnam-plant-disease-detection.git ~/app
cd ~/app

# Cấp quyền chạy script setup
chmod +x deployment/scripts/setup-k3s.sh

# Cấu hình biến môi trường theo đúng thông tin DuckDNS và Email Let's Encrypt trong kế hoạch
export DUCKDNS_SUBDOMAIN="plant-disease-demo"
export DUCKDNS_TOKEN="DIEN_TOKEN_DUCKDNS_CUA_BAN"
export CERT_EMAIL="team@example.com"

# Chạy script setup k3s
./deployment/scripts/setup-k3s.sh
```

**Các tác vụ script này thực hiện:**
- Cài đặt **k3s Server** kèm Ingress Controller Traefik.
- Cài đặt **Helm 3** và **cert-manager** bản `v1.16.2` phục vụ HTTPS.
- Tạo cronjob Systemd tự động gọi DuckDNS cập nhật IP cho domain `plant-disease-demo.duckdns.org` cứ sau mỗi 5 phút.

### 6.3. Kiểm tra k3s trên VM
```bash
kubectl get nodes
# Trạng thái node plant-demo-k3s phải là Ready

kubectl get pods -n cert-manager
# Có 3 pod của cert-manager trạng thái Running
```

---

## Bước 7: Cấu hình Secrets trên GitHub Repository

Để kích hoạt luồng tự động build-push-deploy khi push code lên nhánh `main`, bạn hãy cấu hình các Action Secrets sau tại repo GitHub (`nh-atuan/ml-vietnam-plant-disease-detection`):

1. Vào repo GitHub -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
2. Nhập các cặp Key-Value sau (không chứa dấu cách thừa ở đầu/cuối):

| Tên Secret trên GitHub | Giá trị cần điền |
|---|---|
| `GCP_VM_HOST` | Địa chỉ IP tĩnh ngoại vi của máy ảo (ví dụ: `35.240.231.12`) |
| `GCP_VM_USER` | Tên user kết nối SSH (ví dụ: `pearspringmind`) |
| `GCP_VM_SSH_KEY` | Copy toàn bộ nội dung file khóa bí mật `~/.ssh/k3s_deploy_key` trên máy cá nhân |
| `JWT_SECRET_KEY` | Tạo chuỗi JWT ngẫu nhiên bảo mật (ví dụ chạy lệnh `openssl rand -hex 32` để lấy chuỗi) |
| `POSTGRES_USER` | `admin` |
| `POSTGRES_PASSWORD` | Nhập mật khẩu database tự chọn mạnh |
| `MINIO_ACCESS_KEY` | Nhập key kết nối MinIO tự chọn (ví dụ: `minioadminuser`) |
| `MINIO_SECRET_KEY` | Nhập mật khẩu kết nối MinIO tự chọn |
| `CERT_EMAIL` | `team@example.com` |

---

## Bước 8: Upload Mô hình YOLOv8-seg ONNX vào PVC

Do backend Deployment trong Helm chart luôn mount một PVC tên là `plant-disease-models` tại thư mục `/models`, bạn cần nạp thủ công tệp mô hình và file nhãn bệnh vào PVC này để backend có thể khởi chạy thành công.

### 8.1. Sao chép thư mục models từ máy cá nhân lên thư mục tạm của VM
Tại thư mục gốc dự án trên **máy cá nhân (Local)**, chạy lệnh:
```bash
# Đảm bảo bạn đang có sẵn file models/yolo26_quantized.onnx và models/class_names.json ở máy local
scp -i ~/.ssh/k3s_deploy_key -r models pearspringmind@35.240.231.12:/tmp/models
```

### 8.2. Đưa tệp mô hình vào PVC trên máy ảo VM
Đăng nhập vào máy ảo qua SSH, chạy các lệnh sau để khởi tạo PVC và nạp file vào:

```bash
# 1. Tạo namespace plant-disease trước
kubectl create namespace plant-disease --dry-run=client -o yaml | kubectl apply -f -

# 2. Tạo một Pod tạm để mount volume `plant-disease-models`
kubectl -n plant-disease apply -f - <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: model-loader
spec:
  restartPolicy: Never
  volumes:
    - name: models
      persistentVolumeClaim:
        claimName: plant-disease-models
  containers:
    - name: model-loader
      image: busybox:1.36
      command: ["sh", "-c", "mkdir -p /models && sleep 3600"]
      volumeMounts:
        - name: models
          mountPath: /models
EOF

# 3. Đợi Pod chuyển sang Ready
kubectl -n plant-disease wait --for=condition=Ready pod/model-loader --timeout=60s

# 4. Sao chép mô hình và nhãn bệnh từ thư mục tạm /tmp/models vào trong Volume
kubectl -n plant-disease cp /tmp/models/yolo26_quantized.onnx model-loader:/models/yolo26_quantized.onnx
kubectl -n plant-disease cp /tmp/models/class_names.json model-loader:/models/class_names.json

# 5. Kiểm tra tệp tin đã ở trong PVC
kubectl -n plant-disease exec model-loader -- ls -la /models

# 6. Xóa Pod tạm
kubectl -n plant-disease delete pod model-loader
```

---

## Bước 9: Triển khai Ứng dụng (Deploy)

### Cách 1: Deploy Tự động qua CI/CD GitHub Actions (Khuyên dùng)
Bạn chỉ cần thực hiện push code lên nhánh chính `main` từ máy local:
```bash
git add .
git commit -m "ci: deploy plant disease app to k3s"
git push origin main
```
GitHub Actions sẽ tự động kích hoạt workflow [deploy.yml](../../.github/workflows/deploy.yml). Pipeline sẽ tự động thực hiện chạy test, build Docker images cho frontend/backend, push lên registry của GitHub, SSH vào máy ảo GCP và ra lệnh cho Helm cài đặt.

### Cách 2: Deploy thủ công bằng lệnh Helm trên máy ảo VM
Nếu muốn chạy trực tiếp trên VM (ví dụ để test nhanh):
```bash
# SSH vào máy ảo VM và chạy lệnh sau trong thư mục ~/app
helm upgrade --install plant-disease ./deployment/helm \
  --namespace plant-disease \
  --create-namespace \
  --set global.domain="plant-disease-demo.duckdns.org" \
  --set ingress.tlsEmail="team@example.com" \
  --set backend.image.tag="latest" \
  --set frontend.image.tag="latest" \
  --set-string secretsRaw.jwt-secret="mat_khau_jwt_sieu_manh" \
  --set-string secretsRaw.postgres-user="admin" \
  --set-string secretsRaw.postgres-password="mat_khau_db_tu_chon" \
  --set-string secretsRaw.minio-access-key="minioadminuser" \
  --set-string secretsRaw.minio-secret-key="mat_khau_minio_tu_chon" \
  --wait --timeout 10m
```

---

## Bước 10: Kiểm tra và Đánh giá (Verification)

Sau khi quá trình deploy hoàn thành, hãy thực hiện kiểm tra hoạt động các pod và endpoint:

1. **Kiểm tra pods**:
   ```bash
   kubectl get pods -n plant-disease
   ```
   *Yêu cầu*: Các pod `backend`, `frontend`, `postgres`, `minio`, `redis` đều đang `Running` và có trạng thái `1/1 Ready`.

2. **Kiểm tra Ingress**:
   ```bash
   kubectl get ingress -n plant-disease
   ```
   *Yêu cầu*: Có bản ghi ingress trỏ tới host `plant-disease-demo.duckdns.org`.

3. **Truy cập trình duyệt**:
   - Giao diện Web: `https://plant-disease-demo.duckdns.org`
   - API Health Check: `https://plant-disease-demo.duckdns.org/health`
   - Tài liệu API: `https://plant-disease-demo.duckdns.org/docs`

---

## Tắt máy ảo để tiết kiệm chi phí khi không hoạt động
Đồ án chỉ dùng để kiểm tra hoặc demo trong một khoảng thời gian nhất định. Để tránh lãng phí chi tiêu thẻ, bạn có thể tắt máy ảo khi không sử dụng bằng lệnh trên máy cá nhân hoặc qua GCP Console:
- **Tắt VM**: `gcloud compute instances stop plant-demo-k3s --zone=asia-southeast1-b`
- **Bật lại VM**: `gcloud compute instances start plant-demo-k3s --zone=asia-southeast1-b`
*(Khi bật lại, các pod Kubernetes và cronjob tự động cập nhật IP DuckDNS sẽ tự động khởi chạy và phục hồi về trạng thái hoạt động bình thường)*.
