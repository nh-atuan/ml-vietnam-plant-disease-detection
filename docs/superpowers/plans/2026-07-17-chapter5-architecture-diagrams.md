# Chapter 5 Architecture Diagrams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sửa trình sinh Excalidraw để tạo hai sơ đồ chính xác, ổn định và đủ chất lượng chèn vào Chương 5.

**Architecture:** `scripts/generate_excalidraw.py` cung cấp các hàm tạo phần tử Excalidraw xác định và hai hàm dựng sơ đồ logic/triển khai. CLI mặc định ghi bốn artifact vào `docs`; kiểm thử đọc JSON để khóa nội dung, style và tính xác định trước khi render trực quan.

**Tech Stack:** Python 3.12, `unittest`, Excalidraw JSON v2, Playwright renderer của kỹ năng Excalidraw.

## Global Constraints

- Hai output: `architecture_diagram.excalidraw` và `deployment_architecture_diagram.excalidraw`.
- Tiếng Việt là ngôn ngữ chính; giữ nguyên endpoint, artifact và tên công nghệ.
- Tất cả phần tử dùng `roughness: 0`, `opacity: 100`; text dùng `fontFamily: 3`.
- Không mô tả RAG, vector database, YOLOv8 hoặc Redis như cache đang hoạt động.
- Script không dùng random hoặc timestamp; hai lần chạy phải tạo byte JSON giống nhau.

---

### Task 1: Khóa hợp đồng đầu ra bằng kiểm thử

**Files:**
- Create: `tests/test_generate_excalidraw.py`
- Test: `scripts/generate_excalidraw.py`

**Interfaces:**
- Consumes: `generate_all(output_dir: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]`.
- Produces: kiểm thử nội dung, style, tính xác định và tính toàn vẹn ID của hai JSON.

- [ ] **Step 1: Viết kiểm thử thất bại**

Tạo test bằng `unittest` gọi `generate_all()` trong hai thư mục tạm, xác nhận hai JSON giống nhau, có các nhãn `YOLO26-seg quantized`, `diseases.json`, `/api/v1/predict`, `GCP VM`, `k3s`, `Traefik`, `GHCR`, `Helm`; đồng thời không chứa `RAG`, `Vector DB`, `YOLOv8`. Duyệt toàn bộ phần tử để kiểm tra `roughness == 0`, `opacity == 100`, text có `fontFamily == 3`, và mọi ID là duy nhất.

- [ ] **Step 2: Chạy test để xác nhận RED**

Run: `python -m unittest tests.test_generate_excalidraw -v`

Expected: FAIL vì `generate_all` chưa tồn tại và script hiện còn sinh dữ liệu ngẫu nhiên.

- [ ] **Step 3: Commit kiểm thử**

```bash
git add tests/test_generate_excalidraw.py
git commit -m "test: define architecture diagram contract"
```

### Task 2: Viết lại generator xác định cho hai sơ đồ

**Files:**
- Modify: `scripts/generate_excalidraw.py`
- Generate: `docs/architecture_diagram.excalidraw`
- Generate: `docs/deployment_architecture_diagram.excalidraw`
- Test: `tests/test_generate_excalidraw.py`

**Interfaces:**
- Produces: `build_application_architecture() -> dict`, `build_deployment_architecture() -> dict`, `generate_all(output_dir: Path) -> tuple[Path, Path]`, và CLI `python scripts/generate_excalidraw.py --output-dir docs`.

- [ ] **Step 1: Tạo primitives Excalidraw xác định**

Thay `random`/`time` bằng seed tính từ ID, chuẩn hóa metadata, và tạo helper cho text, rectangle, container, arrow, divider và evidence badge. Mọi helper phải áp dụng palette, `roughness: 0`, `opacity: 100`, `fontFamily: 3`.

- [ ] **Step 2: Dựng bản kiến trúc ứng dụng**

Tạo luồng Người dùng → Next.js → FastAPI và fan-out tới ONNX Runtime, PostgreSQL, MinIO, Expert Knowledge Base. Thêm endpoint thật và artifact `/models/yolo26_quantized.onnx`, `plant-disease-images`, `diseases.json` làm evidence.

- [ ] **Step 3: Dựng bản kiến trúc triển khai**

Tạo các biên GCP VM → k3s → namespace, luồng DuckDNS/HTTPS → Traefik → frontend/backend, workload dữ liệu/PVC và luồng GitHub Actions → GHCR → Helm. Redis chỉ mang nhãn `dịch vụ đã triển khai`.

- [ ] **Step 4: Chạy test để xác nhận GREEN**

Run: `python -m unittest tests.test_generate_excalidraw -v`

Expected: PASS toàn bộ test.

- [ ] **Step 5: Sinh artifact chính thức và kiểm tra lặp**

Run twice: `python scripts/generate_excalidraw.py --output-dir docs`

Expected: tạo hai file `.excalidraw`; `sha256sum` không đổi giữa hai lần.

### Task 3: Render, kiểm tra trực quan và tinh chỉnh

**Files:**
- Modify: `scripts/generate_excalidraw.py`
- Regenerate: `docs/architecture_diagram.excalidraw`
- Regenerate: `docs/deployment_architecture_diagram.excalidraw`
- Generate: `docs/architecture_diagram.png`
- Generate: `docs/deployment_architecture_diagram.png`

**Interfaces:**
- Consumes: hai JSON Excalidraw từ Task 2.
- Produces: hai PNG đã kiểm tra trực quan và sẵn sàng dùng trong báo cáo.

- [ ] **Step 1: Render cả hai sơ đồ**

Run:

```bash
/home/pearspringmind/.codex/skills/excalidraw-diagram/references/.venv/bin/python \
  /home/pearspringmind/.codex/skills/excalidraw-diagram/references/render_excalidraw.py \
  docs/architecture_diagram.excalidraw --output docs/architecture_diagram.png --width 1920

/home/pearspringmind/.codex/skills/excalidraw-diagram/references/.venv/bin/python \
  /home/pearspringmind/.codex/skills/excalidraw-diagram/references/render_excalidraw.py \
  docs/deployment_architecture_diagram.excalidraw --output docs/deployment_architecture_diagram.png --width 1920
```

Expected: hai PNG render thành công.

- [ ] **Step 2: Xem và audit cả hai PNG**

Kiểm tra thứ tự đọc, cỡ chữ ở chiều rộng trang A4, arrow routing, text overflow, khoảng cách, độ cân bằng và tính chính xác nội dung.

- [ ] **Step 3: Sửa mọi lỗi nhìn thấy và render lại**

Điều chỉnh tọa độ/kích thước/đường mũi tên trong generator, chạy test, sinh JSON, render và xem lại. Lặp đến khi không còn chữ tràn, chồng lấp, mũi tên cắt hộp hoặc vùng trống mất cân đối.

- [ ] **Step 4: Xác minh cuối**

Run:

```bash
python -m unittest tests.test_generate_excalidraw -v
python scripts/generate_excalidraw.py --output-dir docs
git diff --check
```

Expected: test PASS, generator thành công, không có whitespace error.
