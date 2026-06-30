# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ - DATA PHASE
## Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)

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

## Tổng quan mốc thời gian (Data Phase)

| Mốc | Thời điểm | Phase | Nội dung yêu cầu nộp | Trạng thái |
|-----|-----------|-------|----------------------|------------|
| Tuần 3 | *(đã qua)* | — | Nộp đề cương (1–2 trang) | Hoàn thành |
| Tuần 6 | *(đã qua)* | 1–2 | **Data + EDA + Preprocessing** – Dữ liệu sạch, phân tích khám phá, tiền xử lý ảnh | Hoàn thành |

---

## PHASE 1 — Thu thập & Chuẩn bị Dữ liệu
> **Tuần 3 → Tuần 6** | *(Đã hoàn thành)*

### Mục tiêu Phase 1
- Tìm kiếm, download, cào bằng API hoặc bot & hợp nhất các bộ dataset (Rice, Coffee)
- Chuẩn hóa nhãn, tạo mask, loại ảnh lỗi/trùng lặp
- Kiểm soát imbalance, chia train/val/test
- Thiết lập cấu trúc thư mục project & version control

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 1.1 | Tìm kiếm, download & merge dataset lúa và cà phê | **Đàm Đạt** | `data/raw/` |
| 1.2 | Tổng hợp viết báo cáo tiến độ lần 1 (phần dữ liệu) | **Tuấn Anh** | Phần Thu thập & Chuẩn bị Dữ liệu trong báo cáo |
| 1.3 | Kiểm tra dữ liệu và kiểm duyệt báo cáo tiến độ lần 1 | **Anh Tuấn** | Dữ liệu và báo cáo được kiểm duyệt |

### Kết quả đạt được

| Hạng mục | Mô tả |
|----------|-------|
| Dataset | 7.300 ảnh (lúa: 3.421, cà phê: 3.879), 8 lớp bệnh (`Healthy`, `BrownSpot`, `Hispa`, `LeafBlast`, `LeafMiner`, `PowderyMildew`, `Rust`, `AlgalLeafSpot`), chia 70/15/15 |
| Metadata | `preprocessing_config.json`, `normalization_stats.json` |
| Repo | Cấu trúc thư mục rõ ràng, README có hướng dẫn |
| Tài liệu | Báo cáo tiến độ lần 1 hoàn chỉnh |

---

## PHASE 2 — Tiền xử lý & EDA
> **Tuần 4 → Tuần 6**  | *(Đã hoàn thành)*

### Mục tiêu Phase 2
- Tiền xử lý ảnh: resize, normalize, chuẩn hóa màu (canvas 256×256, padding giữ tỉ lệ)
- Xây dựng pipeline augmentation (RandomResizedCrop, Flip, ColorJitter, MixUp, CutMix,...)
- Phân tích khám phá dữ liệu (EDA) toàn diện: phân phối lớp, kích thước ảnh, độ sáng, cặp bệnh dễ nhầm

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 2.1 | EDA: phân phối lớp, thống kê, visualization, nhận diện cặp bệnh dễ nhầm | **Xuân Trí** | Notebook EDA + biểu đồ |
| 2.2 | Pipeline tiền xử lý & augmentation (chuẩn hóa nhãn, chia split, resize, normalize...) | **Anh Tuấn** | Notebook Preprocessing, `data/processed/`, `data/splits/` |
| 2.3 | Tổng hợp insight, viết báo cáo phần Tiền xử lý & EDA | **Tống Phúc** | Phần EDA trong báo cáo tiến độ lần 1 |

### Kết quả đạt được

| Hạng mục | Mô tả |
|----------|-------|
| Notebook EDA | Biểu đồ phân phối, Bhattacharyya distance, confusion pairs |
| Script tiền xử lý | Pipeline đầy đủ từ raw → processed (7.149 ảnh sạch) |
| Insight | Cặp dễ nhầm: BrownSpot↔LeafBlast, AlgalLeafSpot↔Rust |
| Augmentation | MixUp (α=0.4), CutMix (α=1.0), WeightedRandomSampler |

---

## Đề xuất Điểm Sáng Tạo liên quan đến Data

| # | Ý tưởng sáng tạo | Phase | Người phụ trách | Giá trị mang lại |
|---|-----------------|-------|-----------------|-----------------|
| S1 | **Human-in-the-loop Labeling Tool** (Streamlit): AI pre-label bằng Gemma 4 + kiểm duyệt thủ công, điều hướng bàn phím, phát hiện trùng MD5 *(đã hoàn thành)* | 1–2 | Tất cả | Pipeline thu thập dữ liệu tiếng Việt độc đáo, tái sử dụng được |
| S4 | **Instance Segmentation** thay vì classification: tạo masks thực địa, xác định vùng bệnh + nhãn cùng lúc *(đã xây dựng mask)* | 3+4 | **Tất cả** | Bài toán phong phú hơn, phù hợp ảnh thực địa nhiều lá |

---

## Tổng hợp công việc (Data Phase)

| Thành viên | Phase 1 | Phase 2 | Sáng tạo |
|-----------|---------|---------|----------|
| **Lê Xuân Trí** | — | EDA (2.1) | — |
| **Đàm Tiến Đạt** | Dataset (1.1) | — | — |
| **Tống Thanh Phúc** | — | Báo cáo EDA (2.3) | — |
| **Dương Tuấn Anh** | Báo cáo P1 (1.2) | — | — |
| **Nguyễn Hồ Anh Tuấn** | Kiểm duyệt (1.3) | Preprocessing (2.2) | — |

---

## Quy ước làm việc nhóm

- **Git workflow:** feature branch theo task → PR → review trước khi merge vào `main`
- **Họp nhóm:** ít nhất 1 lần/tuần để sync tiến độ, báo sớm blocker
- **Môi trường:** dùng chung `requirements.txt`, tạo virtual env riêng
- **Naming:** `notebooks/<phase>_<topic>_<author>.ipynb`; script đặt tên theo chức năng trong `src/`
- **Tracking:** cập nhật trạng thái task trong file này hoặc GitHub Issues
