# Runbook: Deploy to Production (k3s)

## Prerequisites

- GCP VM running Ubuntu 22.04 LTS
- Domain configured in DuckDNS (`plant-disease-demo.duckdns.org`)
- GitHub Container Registry (GHCR) access

## Step 1: Prepare SSH Key

```bash
# Generate SSH key (if not already done)
ssh-keygen -t ed25519 -C "k3s-deploy" -f ~/.ssh/k3s_deploy_key

# Copy to GCP VM
gcloud compute ssh --zone=asia-southeast1-b plant-disease-k3s -- -t "mkdir -p ~/.ssh && echo '$(cat ~/.ssh/k3s_deploy_key.pub)' >> ~/.ssh/authorized_keys"
```

## Step 2: Setup k3s Cluster

```bash
# SSH into VM and run setup
chmod +x deployment/scripts/setup-k3s.sh
DUCKDNS_TOKEN="your-token" CERT_EMAIL="your@email.com" ./deployment/scripts/setup-k3s.sh
```

## Step 3: Configure GitHub Secrets

Configure these in GitHub repository settings before using `.github/workflows/deploy.yml`:

```text
GCP_VM_HOST
GCP_VM_USER
GCP_VM_SSH_KEY
JWT_SECRET_KEY
POSTGRES_USER
POSTGRES_PASSWORD
MINIO_ACCESS_KEY
MINIO_SECRET_KEY
```

## Step 4: Build & Push Images

```bash
# Login to GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Build & push backend
docker build -t ghcr.io/hcmus-ml-plant-disease-detection/plant-backend:$(git rev-parse --short HEAD) -f backend/Dockerfile .
docker push ghcr.io/hcmus-ml-plant-disease-detection/plant-backend:$(git rev-parse --short HEAD)

# Build & push frontend
docker build -t ghcr.io/hcmus-ml-plant-disease-detection/plant-frontend:$(git rev-parse --short HEAD) --build-arg NEXT_PUBLIC_API_BASE_URL=https://plant-disease-demo.duckdns.org/api/v1 ./frontend
docker push ghcr.io/hcmus-ml-plant-disease-detection/plant-frontend:$(git rev-parse --short HEAD)
```

## Step 5: Deploy via Helm

```bash
# Update image tags in values.yaml
export BACKEND_TAG=$(git rev-parse --short HEAD)
export FRONTEND_TAG=$(git rev-parse --short HEAD)

# Deploy
helm upgrade --install plant-disease ./deployment/helm \
  --namespace plant-disease \
  --create-namespace \
  --set backend.image.tag=$BACKEND_TAG \
  --set frontend.image.tag=$FRONTEND_TAG \
  --wait --timeout 10m
```

## Step 6: Upload Model Artifacts to PVC

The backend mounts model files from the `plant-disease-models` PVC at `/models`.
After the first Helm deploy creates the PVC, copy the model files into it:

```bash
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

kubectl -n plant-disease cp models/yolo26_quantized.onnx model-loader:/models/yolo26_quantized.onnx
kubectl -n plant-disease cp models/class_names.json model-loader:/models/class_names.json
kubectl -n plant-disease delete pod model-loader
```

## Step 7: Verify

```bash
kubectl -n plant-disease get all
helm list -n plant-disease
curl -sf https://plant-disease-demo.duckdns.org/health
curl -sf https://plant-disease-demo.duckdns.org/api/v1/knowledge
```
