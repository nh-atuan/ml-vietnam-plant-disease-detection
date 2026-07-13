#!/bin/bash
# Script verify Database & Storage trên K3s VM
# Run this on the target VM after deployment

set -e

NAMESPACE="${1:-plant-disease}"

echo "=================================================="
echo "Kiểm tra tính toàn vẹn Storage & Database (K3s)"
echo "Namespace: $NAMESPACE"
echo "=================================================="

echo -e "\n1. Kiểm tra trạng thái PersistentVolumeClaims (PVCs):"
kubectl -n "$NAMESPACE" get pvc
if kubectl -n "$NAMESPACE" get pvc | grep -q "Pending"; then
    echo "❌ WARNING: Có PVC đang ở trạng thái Pending!"
else
    echo "✅ Tất cả PVC đều Bound thành công."
fi

echo -e "\n2. Kiểm tra Probes và Pod Health:"
kubectl -n "$NAMESPACE" get pods -l 'app.kubernetes.io/component in (backend, frontend)'
kubectl -n "$NAMESPACE" get pods -l 'app in (postgres, minio, redis)'

echo -e "\n3. Kiểm tra PostgreSQL (Liveness & Backup):"
PG_POD=$(kubectl -n "$NAMESPACE" get pod -l app=postgres -o jsonpath="{.items[0].metadata.name}")
if kubectl -n "$NAMESPACE" exec "$PG_POD" -- pg_isready -U admin -d plant_disease; then
    echo "✅ PostgreSQL sẵn sàng (pg_isready: OK)"
else
    echo "❌ PostgreSQL KHÔNG sẵn sàng!"
fi

echo "Kiểm tra CronJob Backup:"
kubectl -n "$NAMESPACE" get cronjob

echo -e "\n4. Kiểm tra MinIO (Liveness):"
MINIO_POD=$(kubectl -n "$NAMESPACE" get pod -l app=minio -o jsonpath="{.items[0].metadata.name}")
if kubectl -n "$NAMESPACE" exec "$MINIO_POD" -- curl -sf http://localhost:9000/minio/health/live >/dev/null; then
    echo "✅ MinIO sẵn sàng (Liveness: OK)"
else
    echo "❌ MinIO KHÔNG sẵn sàng!"
fi

echo -e "\n5. Kiểm tra Redis (Liveness):"
REDIS_POD=$(kubectl -n "$NAMESPACE" get pod -l app=redis -o jsonpath="{.items[0].metadata.name}")
if kubectl -n "$NAMESPACE" exec "$REDIS_POD" -- redis-cli ping | grep -q "PONG"; then
    echo "✅ Redis sẵn sàng (PING: PONG)"
else
    echo "❌ Redis KHÔNG sẵn sàng!"
fi

echo -e "\n=================================================="
echo "Hoàn thành kiểm tra!"
echo "=================================================="
