# BÁO CÁO CUỐI KỲ

Xây dựng và Triển khai Hệ thống Học máy Ứng dụng

## CẤU TRÚC BÁO CÁO CUỐI KỲ

Báo cáo phải được tổ chức như sau:

### THÔNG TIN NHÓM VÀ PHÂN CÔNG CÔNG VIỆC

Liệt kê các thành viên trong nhóm và mô tả ngắn gọn vai trò, đóng góp của từng người trong đồ án.

| Họ và tên | MSSV | Phân công công việc |
|---|---|---|
| Nguyễn Văn A | 20XXX | Phụ trách thu thập dữ liệu. |
| Trần Thị B | 20XXX | Phụ trách huấn luyện mô hình, phân tích kết quả. |
| … | … | … |

#### Chương 1: Giới thiệu

- **Phân tích Vấn đề (Problem Definition):** Mô tả chi tiết bài toán, làm rõ tính cấp thiết và ý nghĩa của vấn đề trong bối cảnh thực tiễn Việt Nam.
- **Mục tiêu của Đồ án:** Trình bày các mục tiêu cụ thể mà nhóm hướng tới giải quyết.
- **Tổng quan về Phương pháp:** Mô tả ngắn gọn cách tiếp cận tổng thể, từ thu thập dữ liệu đến triển khai sản phẩm.

#### Chương 2: Thu thập và Phân tích Dữ liệu

- **Nguồn và Phương pháp Thu thập:**
  - Trình bày nguồn dữ liệu (API, scraping, tự tạo,…).
  - Mô tả chi tiết quy trình và công cụ thu thập, định dạng lưu trữ.
- **Tiền xử lý và Làm sạch:**
  - Mô tả các bước đã thực hiện: xử lý nhiễu, dữ liệu thiếu, chuẩn hóa, biến đổi.
- **Phân tích Khám phá Dữ liệu (EDA):**
  - Trình bày các thống kê mô tả, phân tích phân bố nhãn, và mối quan hệ giữa các thuộc tính.
  - Sử dụng biểu đồ, bảng để minh họa các phát hiện quan trọng về dữ liệu.
  - Phân tích chất lượng dữ liệu và cách xử lý các vấn đề (ngoại lệ, trùng lặp).

#### Chương 3: Lựa chọn và Huấn luyện Mô hình

- **Chuẩn bị Dữ liệu cho Mô hình:**
  - Nêu rõ tỷ lệ chia tập Train/Validation/Test và lý do.
  - Tóm tắt các bước tiền xử lý cuối cùng trước khi đưa vào mô hình.
- **Lựa chọn và Kiến trúc Mô hình:**
  - Trình bày và so sánh ít nhất 3 mô hình đã thử nghiệm.
  - Lý giải lý do lựa chọn. Với mô hình Deep Learning, vẽ sơ đồ và mô tả kiến trúc chi tiết.
- **Cấu hình Huấn luyện:**
  - Mô tả hàm mất mát, thuật toán tối ưu, và các siêu tham số chính.
  - Trình bày phương pháp tinh chỉnh tham số (Grid Search, Random Search,…).

#### Chương 4: Kết quả và Thảo luận

- **Kết quả Thực nghiệm:**
  - Trình bày biểu đồ quá trình học (Learning Curves: Loss, Accuracy,…) trên tập Train và Validation, kèm theo nhận xét.
  - Báo cáo các chỉ số đánh giá (Accuracy, Precision, Recall, F1-Score, RMSE,…) trên tập Test.
  - Hiển thị và phân tích ma trận nhầm lẫn (Confusion Matrix).
- **So sánh và Thảo luận:**
  - Lập bảng so sánh hiệu năng giữa các mô hình đã thử nghiệm.
  - Phân tích hiện tượng Overfitting/Underfitting và các biện pháp đã áp dụng.
  - Phân tích các trường hợp dự đoán sai điển hình và đưa ra giả thuyết nguyên nhân.

#### Chương 5: Xây dựng và Triển khai Ứng dụng

- **Kiến trúc Hệ thống:** Mô tả kiến trúc tổng thể của ứng dụng, cách mô hình được đóng gói và tích hợp.
- **Giao diện và Chức năng:**
  - Mô tả giao diện người dùng (UI) và các chức năng chính.
  - Cung cấp hình ảnh chụp màn hình ứng dụng.
- **Triển khai:**
  - Nêu rõ nền tảng triển khai (cloud công khai hoặc local).
  - Nếu triển khai trên **nền tảng cloud công khai**: Cung cấp đường dẫn URL của ứng dụng đang hoạt động.
  - Nếu triển khai **local**: Cung cấp hướng dẫn chi tiết (các bước cài đặt, câu lệnh chạy) để có thể chạy ứng dụng trên máy local.

#### Chương 6: Kết luận

- **Tóm tắt Kết quả:** Tóm tắt lại những gì đồ án đã đạt được so với mục tiêu ban đầu.
- **Hạn chế:** Thẳng thắn chỉ ra những hạn chế của mô hình và ứng dụng.
- **Hướng phát triển:** Đề xuất các ý tưởng để cải thiện và phát triển đồ án trong tương lai.

#### Phụ lục

- **Tài liệu tham khảo:** Liệt kê các bài báo, sách, tài nguyên đã tham khảo.

## YÊU CẦU VỀ TRÌNH BÀY

1. **Văn phong:** Khoa học, khách quan, súc tích.
2. **Hình ảnh/Bảng biểu:** Mọi hình ảnh, bảng biểu phải được đánh số, có chú thích rõ ràng và được tham chiếu trong nội dung báo cáo.
3. **Trích dẫn:** Trích dẫn đầy đủ các nguồn tài liệu, kiến trúc mô hình tham khảo.
4. **Giới hạn:** Báo cáo không nên vượt quá **30 trang** (không bao gồm phụ lục) và khoảng **7000 từ** để đảm bảo tính cô đọng.

## CÁC SẢN PHẨM PHẢI NỘP

1. **Báo cáo Đồ án:** Tài liệu hoàn chỉnh theo cấu trúc trên.
2. **Mã nguồn:** Toàn bộ code (tiền xử lý, huấn luyện, ứng dụng web).
3. **Mô hình đã huấn luyện:** Các file trọng số của mô hình tốt nhất.
4. **Slide:** Slide trình bày cho buổi bảo vệ cuối kỳ.

**Tổ chức lưu trữ trên Cloud:** Tổ chức lưu trữ các sản phẩm (mã nguồn, mô hình đã huấn luyện) trên một nền tảng cloud (ví dụ: Google Drive, OneDrive, …).

- **Lưu ý:** Mã nguồn nên được quản lý trên GitHub/GitLab và cung cấp liên kết tới kho chứa công khai (public repository).

## TIÊU CHÍ ĐÁNH GIÁ

| Mục | Trọng số | Đánh giá |
|---|---|---|
| Báo cáo Khoa học & Chiều sâu Lý thuyết | 30% | Phân tích vấn đề sắc bén. Trình bày cơ sở lý thuyết rõ ràng. Quy trình các bước đầy đủ, logic. Phân tích kết quả sâu sắc. |
| Sản phẩm Kỹ thuật (Code & Model) | 30% | Chất lượng code (sạch, hiệu quả, có chú thích). Mức độ đầu tư vào dữ liệu. Hiệu năng của mô hình cuối cùng so với các baseline. |
| Ứng dụng Web | 30% | Ứng dụng mô hình + tích hợp với API hoạt động ổn định, giao diện thân thiện, giải quyết đúng bài toán. |
| Điểm Sáng tạo | 10% | Tạo ra sản phẩm đột phá và có giá trị thực tiễn cao. |
