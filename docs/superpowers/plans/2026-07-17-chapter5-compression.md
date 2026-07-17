# Chapter 5 Compression Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rút Chương 5 từ 14 trang xuống 7--8 trang mà vẫn giữ đủ nội dung và minh chứng thuộc phần việc của Lê Xuân Trí.

**Architecture:** Biên tập lại duy nhất `report/content/ch5_app.tex` theo năm khối nội dung cô đọng. Giảm số float độc lập bằng cách ghép ảnh UI và ảnh vận hành thành các figure nhiều subfigure; giữ ảnh Swagger và Knowledge Base chi tiết trong repository nhưng không đặt thành trang độc lập trong Chương 5.

**Tech Stack:** LaTeX, `graphicx`, `subcaption`, `tabularx`, pdfTeX, BibTeX và Poppler.

## Global Constraints

- Chương 5 phải chiếm 7 hoặc 8 trang theo số trang in trong PDF.
- Giữ Architecture, Auth, Predict, History, Knowledge Base, GCP/k3s/Helm, CI/CD và trạng thái vận hành.
- Giữ URL `https://plant-disease-demo.duckdns.org/`.
- Không xóa hình khỏi repository.
- Mọi bảng Chương 5 phải có đầy đủ đường viền.
- Không có lỗi LaTeX nghiêm trọng, tham chiếu chưa xác định hoặc nội dung bị cắt/tràn.

---

### Task 1: Rút gọn cấu trúc và văn bản Chương 5

**Files:**
- Modify: `report/content/ch5_app.tex`

**Interfaces:**
- Consumes: các ảnh hiện có trong `report/img/ch5/` và citation `onnxruntime2026`, `nextjs2026`, `k3s2026`, `helm2026`.
- Produces: Chương 5 gồm năm subsection: kiến trúc; tích hợp; giao diện; triển khai; đánh giá.

- [x] **Step 1: Ghi nhận baseline**

Run: `pdfinfo report/main.pdf | rg "Pages"`

Expected: toàn báo cáo có 43 trang; mục lục cho thấy Chương 5 từ trang 24 đến 37.

- [x] **Step 2: Viết lại nội dung cô đọng**

Giữ bảng kiến trúc có border, rút luồng chẩn đoán thành một đoạn đánh số nội tuyến, gộp ONNX và Docker vào một subsection, rút Auth/History thành một đoạn flow, gộp phần tải/chụp ảnh với Predict, và rút phần giới hạn thành một đoạn.

- [x] **Step 3: Kiểm tra tính đầy đủ của từ khóa**

Run: `rg -n "ONNX|Docker|JWT|history|camera|MinIO|PostgreSQL|k3s|Helm|Traefik|HTTPS|CI/CD|Kubernetes|plant-disease-demo" report/content/ch5_app.tex`

Expected: mỗi nhóm yêu cầu vẫn xuất hiện ít nhất một lần trong nội dung.

### Task 2: Tối ưu bố trí hình và bảng

**Files:**
- Modify: `report/content/ch5_app.tex`

**Interfaces:**
- Consumes: `web-home.png`, `web-login.png`, `web-predict-coffee-v2.png`, `web-knowledge.png`, `cicd-pipeline-success.png`, `kubernetes-status.png`, `deployment-architecture-gcp-k3s.png`.
- Produces: bốn figure chính; không còn float toàn trang riêng cho Swagger hoặc Knowledge Base chi tiết.

- [x] **Step 1: Ghép ảnh UI**

Tạo một figure hai subfigure cho trang chủ và đăng nhập; tạo một figure hai subfigure cho Predict và danh sách Knowledge Base. Dùng `height` giới hạn và `keepaspectratio` để tránh tràn.

- [x] **Step 2: Ghép minh chứng vận hành**

Tạo một figure hai subfigure cho CI/CD và Kubernetes; caption phải nêu rõ cả hai minh chứng.

- [x] **Step 3: Giữ bảng có border**

Run: `rg -n "tabularx|\\\\hline" report/content/ch5_app.tex`

Expected: các bảng sử dụng khai báo cột có ký tự `|` và mỗi hàng kết thúc bằng `\\ \hline`.

### Task 3: Biên dịch và điều chỉnh tới 7--8 trang

**Files:**
- Modify if required: `report/content/ch5_app.tex`
- Generate: `report/main.pdf`

**Interfaces:**
- Consumes: Chương 5 đã rút gọn từ Task 1--2.
- Produces: PDF A4 hoàn chỉnh với Chương 5 dài 7--8 trang.

- [x] **Step 1: Biên dịch đủ vòng**

Run lần lượt: `pdflatex -interaction=nonstopmode -halt-on-error main.tex`, `bibtex main`, rồi chạy `pdflatex` hai lần.

Expected: các lệnh thoát mã 0.

- [x] **Step 2: Đo phạm vi Chương 5**

Run: `pdftotext -layout main.pdf /tmp/report.txt` và đọc mục lục để lấy trang bắt đầu của Chương 5 và Chương 6.

Expected: hiệu giữa hai số trang là 7 hoặc 8.

- [x] **Step 3: Rà log**

Run: `rg -n "Undefined control sequence|LaTeX Warning:.*undefined|Fatal error|Emergency stop" main.log`

Expected: không có kết quả.

- [x] **Step 4: Render và xem trực quan**

Render toàn bộ phạm vi Chương 5 bằng `pdftoppm`; kiểm tra caption, border bảng, kích thước chữ trong hình, khoảng trắng và nội dung bị cắt.

- [x] **Step 5: Kiểm tra thay đổi**

Run: `git diff --check` và `git status --short`.

Expected: không có whitespace error; chỉ các tệp kế hoạch/nội dung chủ đích thay đổi.
