# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ
## Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)

---

## Thông tin nhóm

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Nguyễn Hồ Anh Tuấn | 23120185 |
| 2 | Lê Xuân Trí | 23120099 |
| 3 | Đàm Tiến Đạt | 23120118 |
| 4 | Tổng Thanh Phúc | 23120158 |
| 5 |Dương Tuấn Anh | 23120208 |

> **Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên

---

## Tổng quan mốc thời gian

| Mốc | Thời điểm | Nội dung yêu cầu nộp |
|-----|-----------|----------------------|
| Tuần 3 | *(đã qua)* | Nộp đề cương (1–2 trang) |
| Tuần 6 | Báo cáo tiến độ lần 1 | **Data + EDA** – Dữ liệu sạch, phân tích khám phá |
| Tuần 10 | Báo cáo tiến độ lần 2 | **Model + Evaluation** – Mô hình đã huấn luyện, đánh giá |
| Tuần cuối | Nộp cuối kỳ | **Deploy + Báo cáo + Slide + Demo** |

---

## PHASE 1 — Thu thập & Chuẩn bị Dữ liệu
> **Tuần 3 → Tuần 6** | **Deadline nộp: Tuần 6 (Báo cáo tiến độ lần 1)**

### Mục tiêu Phase 1
- Tìm kiếm, download, cào bằng API hoặc bot & hợp nhất các bộ dataset (Rice, Coffee)
- Chuẩn hóa nhãn (nếu có), tạo mask, loại    ảnh lỗi/trùng lặp
- Kiểm soát imbalance, chia train/val/test
- Thiết lập cấu trúc thư mục project & version control

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 1.1 | Tìm kiếm, download & merge dataset lúa và cà phê | **Đàm Đạt** | `data/raw/` |
| 1.2 | Tổng hợp viết báo cáo tiến độ lần 1 (dựa trên phần dữ liệu) | **Tuấn Anh** | Phần Thu thập & Chuẩn bị Dữ liệu trong Báo cáo tiến độ lần 1 |
| 1.3 | Kiểm tra dữ liệu và báo cáo tiến độ lần 1 | **Anh Tuấn** | Dữ liệu và báo cáo được kiểm duyệt |

### Kết quả cần đạt cuối Phase 1

| Hạng mục | Mô tả |
|----------|-------|
| Dataset | ~10k–15k ảnh sạch, đã gán nhãn, đã chia split |
| Metadata | File CSV chứa đường dẫn, nhãn, nguồn gốc |
| Repo | Cấu trúc thư mục rõ ràng, README có hướng dẫn |
| Tài liệu báo cáo | Tổng số mẫu, phân phối nhãn, mô tả nguồn |

---

## PHASE 2 — Tiền xử lý & EDA
> **Tuần 4 → Tuần 6** *(song song với Phase 1)* | **Deadline nộp: Tuần 6 (Báo cáo tiến độ lần 1)**

### Mục tiêu Phase 2
- Tiền xử lý ảnh: resize, normalize, chuẩn hóa màu
- Xây dựng pipeline augmentation
- Phân tích khám phá dữ liệu (EDA) toàn diện

### Phân công công việc

| # | Công việc (gợi ý chứ không giới hạn trong đây) | Người phụ trách | Output |
|---|------------------------------------------------|-----------------|--------|
| 2.1 | Khám phá dữ liệu (EDA): Phân phối lớp, thống kê, visualization, nhận diện bệnh dễ nhầm | **Xuân Trí** | Notebook EDA + biểu đồ, hình ảnh |
| 2.2 | Pipeline tiền xử lý ảnh và augmentation (chuẩn hóa nhãn, chia split, resize, normalize, Flip, v.v) | **Anh Tuấn** | Notebook Preprocessing, `data/processed/`, `data/splits/` |
| 2.3 | Tổng hợp insight, viết báo cáo phần Tiền xử lý & EDA (cho Báo cáo tiến độ lần 1) | **Tổng Phúc** | Phần Tiền xử lý & EDA trong Báo cáo tiến độ lần 1|

### Kết quả cần đạt cuối Phase 2

| Hạng mục | Mô tả |
|----------|-------|
| Notebook EDA | Đầy đủ biểu đồ phân phối, visualizations |
| Script tiền xử lý | Có thể chạy pipeline đầy đủ từ raw → ready |
| Insight | Nêu được đặc điểm dữ liệu, bệnh dễ nhầm |
| Tài liệu báo cáo  | Phần Data + EDA cho báo cáo Báo cáo tiến độ lần 1 |
