# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ - FINAL PHASE (BÁO CÁO & VẤN ĐÁP)
## Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa

---

## Thông tin nhóm

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Lê Xuân Trí | 23120099 |
| 2 | Đàm Tiến Đạt | 23120118 |
| 3 | Tống Thanh Phúc | 23120158 |
| 4 | Dương Tuấn Anh | 23120208 |
| 5 | Nguyễn Hồ Anh Tuấn | 23120185 |

> **Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên

---

## Tổng quan mốc thời gian (Final Phase)

| Deadline | Phase | Nội dung yêu cầu nộp | Trạng thái |
|----------|-------|----------------------|------------|
| Hết trưa ngày 17/7 | 7 | **Báo cáo + Slide + Demo** – Hoàn thiện báo cáo 7 bước, slide bảo vệ, đóng gói sản phẩm | Chưa thực hiện |

---

## PHASE 7 — Hoàn thiện Báo cáo, Slide & Demo
> **Deadline: Hết trưa ngày 17/7**

### Mục tiêu Phase 7
- Hoàn thiện báo cáo khoa học đầy đủ 6 chương (7 bước quy trình) theo yêu cầu môn học.
- Chuẩn bị slide bảo vệ súc tích, trực quan, đồng bộ với nội dung báo cáo.
- Đóng gói mã nguồn sạch, tài liệu hóa hướng dẫn cài đặt và load mô hình.
- Quay video demo hoạt động của website ứng dụng trên cloud công khai.
- Tổ chức lưu trữ sản phẩm cuối kỳ khoa học trên nền tảng Cloud.

---

## PHÂN CHIA CÔNG VIỆC CHI TIẾT

Để đảm bảo tính nhất quán và tối ưu hóa hiệu quả làm việc, việc phân chia viết **Báo cáo** và **Slide** được đồng bộ trực tiếp theo các phần việc/mô hình mà từng thành viên đã phụ trách ở các phase trước (Data, Model, Web/DevOps).

### 1. Nguyễn Hồ Anh Tuấn
* **Báo cáo:** Chủ trì và viết **Chương 1: Giới thiệu**
  - **Phân tích Vấn đề (Problem Definition):** Mô tả chi tiết bài toán chẩn đoán bệnh trên lá lúa/cà phê, tính cấp thiết và ý nghĩa thực tiễn tại Việt Nam.
  - **Mục tiêu của Đồ án:** Các mục tiêu cụ thể cần đạt được (độ chính xác, khả năng triển khai thực tế).
  - **Tổng quan về Phương pháp:** Sơ đồ quy trình tổng thể từ dữ liệu, huấn luyện đến triển khai web.
* **Slide:** Soạn slide tương ứng với **Chương 1**.
* **Trách nhiệm phối hợp:** Tổng hợp báo cáo tổng thể, rà soát văn phong, kiểm tra lỗi định dạng và tính nhất quán giữa Báo cáo, Slide và mã nguồn Backend.

### 2. Đàm Tiến Đạt
* **Báo cáo:** Viết **Chương 2: Thu thập và Phân tích Dữ liệu** & **Chương 3: Lựa chọn và Huấn luyện Mô hình**
  - **Chương 2:** Nguồn và phương pháp thu thập dữ liệu (merging dataset lúa & cà phê), các bước tiền xử lý/làm sạch và kết quả phân tích khám phá dữ liệu (EDA).
  - **Chương 3:** Chia tập train/val/test; so sánh kiến trúc 5 mô hình đã thử nghiệm (Mask R-CNN, YOLO26-seg, RF-DETR, MobileSAM, Mask2Former); cấu hình huấn luyện chi tiết; phương pháp tinh chỉnh siêu tham số (RayTune & ASHA).
* **Slide:** Soạn slide tương ứng với **Chương 2** và **Chương 3**.
* **Minh chứng ML phụ trách:**
  - File trọng số của mô hình tốt nhất (`.onnx` và `.pt`).
  - Toàn bộ script export mô hình và script quantization (tối ưu hóa suy luận trên CPU).
  - Viết hướng dẫn load mô hình và chạy thử nghiệm inference cục bộ (Model Card/README tại folder model).

### 3. Tống Thanh Phúc
* **Báo cáo:** Viết **Chương 4: Kết quả và Thảo luận**
  - **Kết quả Thực nghiệm:** Learning curves (Loss, Accuracy, mAP) của quá trình huấn luyện trên các tập dữ liệu; các chỉ số đánh giá (mAP@50, mAP@50:95, mIoU, Dice Score, inference time) trên tập Test.
  - Hiển thị và phân tích ma trận nhầm lẫn (Confusion Matrix) chi tiết.
  - **So sánh và Thảo luận:** Bảng so sánh hiệu năng các mô hình; phân tích hiện tượng Overfitting/Underfitting và cách khắc phục; phân tích các trường hợp dự đoán sai điển hình (confusion pairs) và nguyên nhân.
* **Slide:** Soạn slide tương ứng với **Chương 4**.
* **Trách nhiệm phối hợp:** Cung cấp kết quả load testing, kiểm tra tính toàn vẹn của database SQLModel và lưu trữ ảnh người dùng trên MinIO để bổ sung số liệu thực nghiệm.

### 4. Lê Xuân Trí
* **Báo cáo:** Viết **Chương 5: Xây dựng và Triển khai Ứng dụng**
  - **Kiến trúc Hệ thống:** Sơ đồ kiến trúc tổng thể, cách đóng gói và tích hợp mô hình (FastAPI, Next.js, PostgreSQL, MinIO, ONNX Runtime).
  - **Giao diện và Chức năng:** Hình ảnh chụp màn hình (UI/UX) và luồng hoạt động chính (Auth, Predict, History, Expert Knowledge Base).
  - **Triển khai Cloud:** Mô tả quá trình container hóa (Docker), viết Helm Chart, cài đặt cụm Kubernetes (k3s) trên GCP VM, cấu hình định tuyến ingress qua Traefik và tên miền DuckDNS kèm SSL HTTPS.
* **Slide:** Soạn slide tương ứng với **Chương 5**.
* **Minh chứng Cloud & Storage phụ trách:**
  - Thiết lập và tổ chức thư mục chia sẻ sản phẩm đồ án trên Cloud (Google Drive hoặc OneDrive) một cách khoa học (bao gồm báo cáo PDF, slide, mã nguồn đóng gói ZIP, model weights tốt nhất).
  - Đảm bảo repo GitHub/GitLab công khai được dọn dẹp sạch sẽ, cấu trúc thư mục rõ ràng, đầy đủ file README hướng dẫn chạy thử nghiệm local và các cấu hình DevOps (`deployment/helm/`, `.github/workflows/`).

### 5. Dương Tuấn Anh
* **Báo cáo:** Viết **Chương 6: Kết luận**
  - **Tóm tắt Kết quả:** Đánh giá mức độ hoàn thành so với mục tiêu ban đầu.
  - **Hạn chế:** Các giới hạn của mô hình thực tế và hệ thống ứng dụng web.
  - **Hướng phát triển:** Ý tưởng cải tiến mô hình (tăng cường tập dữ liệu, kiến trúc mới) và mở rộng tính năng ứng dụng.
* **Slide:** Soạn slide tương ứng với **Chương 6**.
* **Video Demo phụ trách:** Quay màn hình và biên tập hoàn chỉnh video demo chạy ứng dụng trên cloud công khai theo các yêu cầu chất lượng (chi tiết bên dưới).

---

## YÊU CẦU CHI TIẾT VIDEO DEMO ỨNG DỤNG (Dương Tuấn Anh phụ trách)

Video demo là minh chứng trực quan cực kỳ quan trọng thể hiện ứng dụng đã được deploy thành công và hoạt động ổn định trên môi trường Cloud. Yêu cầu chi tiết như sau:

- **Thời lượng:** Từ **3 đến 5 phút** (không quá dài dòng, tập trung trực tiếp vào trải nghiệm và tính năng).
- **Định dạng & Chất lượng:** Video độ phân giải tối thiểu **Full HD (1080p)**, tốc độ khung hình **30fps hoặc 60fps**, âm thanh rõ ràng không bị rè.
- **Thuyết minh:** Có **giọng nói thuyết minh (voiceover)** giải thích các bước thực hiện một cách chuyên nghiệp.

---

## KIỂM TRA ĐỐI CHIẾU SẢN PHẨM / MINH CHỨNG YÊU CẦU

Bảng dưới đây đối chiếu giữa yêu cầu sản phẩm của môn học (theo [ml-final-report.md](../project/ml-final-report.md)) và kế hoạch phân công trong `FINAL_PLAN.md` để đảm bảo không bị sót minh chứng:

| Sản phẩm yêu cầu (ml-final-report.md) | Trạng thái trong FINAL_PLAN.md | Người phụ trách chính | Minh chứng cụ thể |
|--------------------------------------|--------------------------------|-----------------------|-------------------|
| **1. Báo cáo Đồ án (PDF)** | **Đầy đủ** (6 chương tương ứng 7 bước quy trình) | Cả nhóm (Tuấn tổng hợp) | File `Bao_cao_Cuoi_Ky.pdf` |
| **2. Mã nguồn (ZIP/GitHub)** | **Đầy đủ** (Quản lý GitHub public, có đóng gói ZIP) | Lê Xuân Trí | Link GitHub public trong báo cáo + File `source_code.zip` |
| **3. Mô hình đã huấn luyện** | **Đầy đủ** (ONNX quantized + PT, kèm hướng dẫn load) | Đàm Tiến Đạt | Checkpoints trên HuggingFace Hub + File `.onnx`/`.pt` trên Cloud |
| **4. Slide thuyết trình** | **Đầy đủ** (Phần slide khớp nội dung viết báo cáo) | Cả nhóm (Phúc/Trí template) | File `Slide_Bao_ve.pdf` |
| **5. Tổ chức lưu trữ Cloud** | **Đầy đủ** (Google Drive/OneDrive lưu toàn bộ sản phẩm) | Lê Xuân Trí | Link thư mục Cloud dùng chung gửi giảng viên |
| **6. Video Demo Web** *(Thêm mới)* | **Đầy đủ** (Video 3-5 phút chất lượng cao, thuyết minh) | Dương Tuấn Anh | File `Video_Demo.mp4` và link YouTube/Drive |

---

## Quy ước làm việc nhóm

1. **Git workflow:** Tạo feature branch riêng cho báo cáo/slide (`docs/report-chapX`, `slides/chapX`), tạo PR và nhờ Nguyễn Hồ Anh Tuấn review trước khi merge vào `main`.
2. **Tiến độ:** Mọi thành viên chủ động hoàn thành phần viết chương báo cáo và slide tương ứng của mình trước **trưa ngày 17/7** để kịp tổng hợp, định dạng LaTeX/Word chuyên nghiệp và rà soát lỗi trước khi nộp.
3. **Chất lượng nội dung:** Mọi hình ảnh, bảng biểu đưa vào báo cáo và slide phải có chú thích rõ ràng, đánh số thứ tự và được trích dẫn nguồn đầy đủ.
