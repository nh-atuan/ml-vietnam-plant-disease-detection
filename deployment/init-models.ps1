# init-models.ps1 — Copy model files vào Docker named volume
#
# NOTE: Script này hiện đã LỖI THỜI (OBSOLETE) và không cần thiết phải chạy nữa.
# Model đã được cấu hình tự động copy vào backend image khi build bằng docker compose.
# 
# Cách dùng (nếu vẫn muốn chạy độc lập):
#   .\deployment\init-models.ps1

$env:DOCKER_HOST = "npipe:////./pipe/docker_engine_linux"

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$MODELS_DIR = Join-Path $PROJECT_ROOT "models"

Write-Host "=== Khoi tao Docker volume cho models ===" -ForegroundColor Cyan
Write-Host "Source: $MODELS_DIR"
Write-Host "Target: Docker volume 'deployment_models_data'"
Write-Host ""

# Kiem tra thu muc models ton tai
if (-not (Test-Path $MODELS_DIR)) {
    Write-Host "[ERROR] Khong tim thay thu muc models: $MODELS_DIR" -ForegroundColor Red
    exit 1
}

# Kiem tra Docker dang chay
try {
    docker ps | Out-Null
} catch {
    Write-Host "[ERROR] Docker khong chay. Hay mo Docker Desktop truoc." -ForegroundColor Red
    exit 1
}

# Tao container tam thoi de copy files vao volume
Write-Host "[1/3] Tao container tam thoi..."
docker run -d --name models-init -v deployment_models_data:/models alpine sleep 60 2>&1 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Khong the tao container. Thu xoa container cu: docker rm -f models-init" -ForegroundColor Red
    exit 1
}

# Copy tung file model vao volume
Write-Host "[2/3] Copy model files vao volume..."
Get-ChildItem -Path $MODELS_DIR -File | ForEach-Object {
    Write-Host "  Copying $($_.Name) ($([math]::Round($_.Length / 1MB, 1)) MB)..."
    docker cp $_.FullName "models-init:/models/$($_.Name)"
}

# Xoa container tam thoi
Write-Host "[3/3] Don dep container tam thoi..."
docker rm -f models-init | Out-Null

Write-Host ""
Write-Host "=== HOAN THANH ===" -ForegroundColor Green
Write-Host "Model files da duoc copy vao volume 'deployment_models_data'."
Write-Host "Gio co the chay: docker compose -f deployment/docker-compose.yml up --build -d"
