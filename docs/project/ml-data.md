# BÁO CÁO VỀ DỮ LIỆU

Xây dựng và Triển khai Hệ thống Học máy Ứng dụng

Một báo cáo cần có các nội dung sau

---

## Giới thiệu bài toán

Trình bày ngắn gọn lại bài toán học máy mà nhóm hướng tới giải quyết

---

## Phương pháp và nguồn thu thập dữ liệu

### Nguồn dữ liệu

- Dữ liệu dựa trên dataset có sẵn? có mở rộng không?
- Từ API?
- Web scraping?
- Khảo sát, biểu mẫu (Google Form, Survey,…)?

### Phương pháp thu thập

- Quy trình thực hiện từng bước
- Công cụ sử dụng
- Định dạng lưu trữ

### Quy trình làm sạch và tiền xử lý dữ liệu

- Loại bỏ nhiễu (noise), trùng lặp (duplicates)
- Loại bỏ hoặc xử lý dữ liệu thiếu (missing values)
- Chuẩn hoá/biến đổi
- Chuyển đổi kiểu dữ liệu
- Kiểm tra sự nhất quán của dữ liệu

### Đảm bảo chất lượng dữ liệu

- Tiêu chí đánh giá dữ liệu tốt cho học máy
- Kiểm tra thủ công / kiểm tra tự động

### Lưu trữ và quản lý dữ liệu

- Nêu rõ cách tổ chức thư mục dữ liệu

---

## Phân tích khám phá dữ liệu (EDA)

Sử dụng bảng, biểu đồ để phân tích dữ liệu

### Thống kê mô tả

- Số lượng mẫu, số thuộc tính, tỉ lệ dữ liệu thiếu
- Các thống kê cơ bản: mean, median, variance, min/max, IQR cho các biến số
- Phân bố dữ liệu theo từng thuộc tính

### Phân tích phân bố nhãn

- Kiểm tra dữ liệu cân bằng hay mất cân bằng (class imbalance)
- Nêu rõ tỉ lệ phần trăm của mỗi lớp hoặc nhóm

### Phân tích mối quan hệ giữa các thuộc tính

- Kiểm tra tương quan giữa các biến (correlation)
- Phát hiện multicollinearity nếu có
- Nhận xét biến nào quan trọng hoặc có ý nghĩa với bài toán

### Kiểm tra chất lượng dữ liệu

- Phát hiện ngoại lệ và dữ liệu bất thường
- Kiểm tra trùng lặp, dữ liệu không hợp lệ hoặc không đồng nhất
- Mô tả cách xử lý hoặc kế hoạch xử lý

### EDA cho dữ liệu phi cấu trúc

- **Ảnh:** thống kê chất lượng ảnh, độ sáng/tối, độ phân giải, sự đa dạng của đối tượng, …

- **Văn bản:**
  - Thống kê độ dài câu/tài liệu
  - Tần suất từ khoá phổ biến
  - Tỉ lệ ký tự đặc biệt, nhiễu
  - …

- **Âm thanh:** phân tích phổ, …
