# Báo cáo Kiểm thử Hệ thống (Integration & Load Testing)

## 1. Kiểm thử Tích hợp (E2E Integration Testing)
Toàn bộ quy trình từ tải ảnh lên đến khi trả về kết quả đã được đóng gói và kiểm thử trên môi trường triển khai thực tế (Kubernetes cluster).

Quá trình kiểm thử E2E (End-to-End) bao gồm 14 luồng test tự động (đã vượt qua 100%), xác nhận các tính năng cốt lõi sau hoạt động ổn định:
- **Kiểm tra tính toàn vẹn Database (SQLModel):** Luồng đăng ký, đăng nhập (auth flow), và tính năng lưu trữ lịch sử chẩn đoán được PostgreSQL ghi nhận chính xác mà không gặp tình trạng mất đồng bộ.
- **Lưu trữ ảnh trên MinIO:** Quy trình upload ảnh từ Frontend lên Cloud storage thông qua backend diễn ra liền mạch. Hệ thống tự động tạo presigned URL để trả về cho người dùng nhanh chóng.

## 2. Kiểm thử Chịu tải (Load Testing)
Kịch bản kiểm thử Locust (`locustfile.py`) được thực hiện mô phỏng phiên làm việc liên tục của nhiều user ảo (đăng nhập -> gọi API `/predict` -> đọc `/history`).

**Kết quả Thực nghiệm:**
- **Thời gian chạy:** 2 phút
- **Số lượng user ảo (Peak):** 5 users
- **Tổng số requests:** 242 requests
- **Tỷ lệ lỗi (Failure Rate):** 0% (không có lỗi HTTP 5xx)
- **Độ trễ API Inference (p95 latency của `/predict`):** 3.2 giây

**Kết luận:**
Việc tích hợp liền mạch giữa FastAPI, PostgreSQL, MinIO và mô hình YOLO26-seg (sử dụng ONNX Runtime trên CPU) đã chứng minh tính thực tiễn. Tốc độ phản hồi đạt chuẩn cho phép (dưới 5 giây) cho môi trường CPU, phù hợp cho ứng dụng AI phục vụ người dùng.
