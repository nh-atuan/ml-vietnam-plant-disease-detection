# Thiết kế sơ đồ kiến trúc Chương 5

## Mục tiêu

Tạo hai sơ đồ Excalidraw chính xác với hệ thống đang vận hành để sử dụng trong Chương 5 của báo cáo: một bản tập trung vào kiến trúc ứng dụng và một bản mở rộng thể hiện lớp triển khai GCP/k3s bao quanh.

## Đầu ra

- `docs/architecture_diagram.excalidraw`: kiến trúc logic của ứng dụng.
- `docs/architecture_diagram.png`: ảnh render của kiến trúc logic.
- `docs/deployment_architecture_diagram.excalidraw`: kiến trúc triển khai mở rộng.
- `docs/deployment_architecture_diagram.png`: ảnh render của kiến trúc triển khai.
- `scripts/generate_excalidraw.py`: nguồn sinh xác định cả hai sơ đồ.

## Bản 1: Kiến trúc ứng dụng

Luồng chính đi từ trên xuống: người dùng trên trình duyệt gửi yêu cầu tới Next.js, Next.js gọi FastAPI bằng HTTP/JSON, rồi FastAPI điều phối bốn nhánh dịch vụ:

1. ONNX Runtime chạy mô hình `YOLO26-seg quantized` từ `/models/yolo26_quantized.onnx`.
2. PostgreSQL lưu người dùng, ảnh và lịch sử chẩn đoán qua SQLModel.
3. MinIO lưu ảnh tải lên trong bucket `plant-disease-images` và trả URL truy cập.
4. Expert Knowledge Base đọc `backend/app/knowledge/diseases.json` để trả triệu chứng, biện pháp xử lý và phòng bệnh theo luật.

Sơ đồ phải thể hiện các endpoint thật `/api/v1/predict`, `/api/v1/knowledge`, `/api/v1/auth` và `/api/v1/history` như bằng chứng kỹ thuật. Không sử dụng thuật ngữ RAG, vector database hoặc YOLOv8 vì không phản ánh triển khai hiện tại.

## Bản 2: Kiến trúc triển khai mở rộng

Lõi ứng dụng được đặt bên trong ba biên lồng nhau: GCP VM, cụm k3s và namespace `plant-disease`. Luồng truy cập công khai đi qua DuckDNS/HTTPS và Traefik Ingress tới frontend hoặc backend theo đường dẫn.

Các workload phải phản ánh manifest Helm thật:

- Frontend Deployment chạy Next.js.
- Backend Deployment chạy FastAPI và ONNX Runtime.
- PostgreSQL, MinIO và Redis chạy dưới dạng workload có lưu trữ bền vững.
- Model PVC gắn mô hình vào `/models` của backend.
- PostgreSQL và MinIO sử dụng PVC; Redis được ghi là dịch vụ đã triển khai, không khẳng định cache đang được gọi trong mã ứng dụng.

Luồng giao hàng đặt ngoài biên runtime: GitHub Actions chạy lint/test, build image, đẩy image lên GHCR, sau đó triển khai bằng Helm qua SSH và kiểm tra smoke test.

## Ngôn ngữ hình ảnh

- Tiếng Việt là ngôn ngữ chính; giữ nguyên tên sản phẩm, endpoint, định dạng và đường dẫn kỹ thuật.
- Dùng palette chính thức của kỹ năng Excalidraw: xanh dương cho luồng/chủ thể chính, tím cho AI, xanh lá cho trạng thái thành công, cam cho điểm vào, đỏ nhạt cho cảnh báo hoặc lưu trữ cần chú ý.
- `roughness: 0`, `opacity: 100`, `fontFamily: 3` cho toàn bộ phần tử.
- Mũi tên phải có hướng rõ, không cắt xuyên hộp và có nhãn cụ thể.
- Bố cục phải đọc được khi đặt toàn chiều rộng trang A4, không có chữ tràn, chồng lấp hoặc vùng trống mất cân đối.

## Tiêu chí chấp nhận

1. Chạy script hai lần tạo JSON có nội dung ổn định, không phụ thuộc thời gian hoặc số ngẫu nhiên.
2. Cả hai file Excalidraw mở được và render thành PNG thành công.
3. Bản logic nêu đúng YOLO26-seg quantized và Knowledge Base JSON theo luật.
4. Bản triển khai thể hiện đúng GCP VM, k3s, Traefik, Helm, GHCR, workload và PVC.
5. Không có thuật ngữ RAG, vector database hoặc mô tả Redis như cache đang hoạt động.
6. Ảnh render vượt qua kiểm tra trực quan về khả năng đọc, căn chỉnh, khoảng cách và đường nối.
