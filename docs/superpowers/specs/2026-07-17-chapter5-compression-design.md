# Thiết kế rút gọn Chương 5

## Mục tiêu

Rút Chương 5 từ 14 trang xuống khoảng 7--8 trang in sau khi biên dịch toàn bộ báo cáo, đồng thời giữ đủ nội dung được giao cho Lê Xuân Trí: kiến trúc và tích hợp mô hình, giao diện và các luồng chính, triển khai GCP/k3s/Helm, CI/CD và minh chứng vận hành.

## Nguyên tắc biên tập

- Giữ các kết luận kỹ thuật có thể đối chiếu trực tiếp với mã nguồn và cấu hình triển khai.
- Loại bỏ diễn giải lặp lại giữa bảng, hình và văn bản.
- Chuyển từ mô tả tuần tự quá chi tiết sang đoạn tóm tắt hoặc danh sách ngắn.
- Không giảm kích thước chữ toàn báo cáo và không làm hình khó đọc chỉ để đạt số trang.
- Giữ đầy đủ đường viền cho các bảng còn lại.
- Không xóa tài sản hình ảnh khỏi repository.

## Cấu trúc nội dung đích

1. **Kiến trúc hệ thống:** giữ sơ đồ triển khai, bảng thành phần rút gọn và luồng chẩn đoán cô đọng.
2. **Đóng gói và tích hợp:** gộp ONNX Runtime và Docker thành một tiểu mục, chỉ giữ các quyết định triển khai quan trọng.
3. **Giao diện và chức năng:** trình bày Auth, tải/chụp ảnh, Predict, History và Knowledge Base; ghép ảnh thành các cụm để giảm trang hình độc lập.
4. **Triển khai cloud:** gộp k3s/Helm, ingress/HTTPS và CI/CD; giữ các thông số lưu trữ và tài nguyên thiết yếu.
5. **Minh chứng và đánh giá:** giữ ảnh CI/CD, trạng thái Kubernetes và đoạn giới hạn triển khai ngắn.

## Chiến lược hình ảnh

- Giữ hình kiến trúc ở kích thước đủ đọc.
- Ghép trang chủ và đăng nhập thành một figure có hai subfigure.
- Ghép kết quả Predict với giao diện Knowledge Base hoặc History khi có ảnh History phù hợp.
- Ghép CI/CD và Kubernetes thành một figure hai subfigure nếu vẫn bảo đảm đọc được thông tin chính.
- Chuyển ảnh Swagger và ảnh Knowledge Base chi tiết sang phụ lục; trong Chương 5 chỉ giữ mô tả API ngắn và ảnh Knowledge Base tổng quan.
- Tránh dùng float toàn trang khi hình có thể trình bày cùng phần giải thích liên quan.

## Ngân sách trang dự kiến

- Kiến trúc và luồng chẩn đoán: 1--1,5 trang.
- ONNX và Docker: 0,5--1 trang.
- Giao diện và chức năng: 2--2,5 trang.
- GCP, k3s, Helm, HTTPS và CI/CD: 2 trang.
- Minh chứng vận hành, đánh giá và giới hạn: 1 trang.

Tổng mục tiêu là 7--8 trang; chấp nhận tối đa 8 trang sau vòng điều chỉnh float cuối cùng.

## Tiêu chí hoàn thành

- Chương 5 chiếm 7 hoặc 8 trang theo số trang in trong mục lục/PDF.
- Nội dung vẫn bao phủ Architecture, Auth, Predict, History, Knowledge Base và Cloud Deployment.
- URL ứng dụng công khai vẫn xuất hiện rõ ràng.
- Hình và bảng đều có caption, label và được tham chiếu trong nội dung.
- Không có lỗi LaTeX nghiêm trọng, tham chiếu chưa xác định hoặc nội dung bị cắt/tràn.
- Các bảng của Chương 5 có đầy đủ đường viền.
