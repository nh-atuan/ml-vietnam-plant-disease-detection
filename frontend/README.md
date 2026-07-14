# Frontend — Plant Disease Detection Web App

Ứng dụng web chẩn đoán bệnh trên lá cây lúa và cà phê tại Việt Nam, xây dựng trên nền tảng Next.js (App Router), React 19 và Tailwind CSS.

---

## ✨ Các Chức Năng Chính

1. **🔬 Phân tích chẩn đoán bệnh lá cây**:
   - Tải ảnh lên qua cơ chế kéo thả (Drag & Drop) hoặc chọn tệp.
   - Hỗ trợ chụp ảnh trực tiếp từ camera của thiết bị di động.
   - Kiểm tra và xác thực file ảnh phía client (dung lượng tối đa 10 MB, định dạng JPEG, PNG, WEBP).
   
2. **🛡️ Kiểm định kết quả & Độ tin cậy (Trust Signals)**:
   - Hiển thị tỷ lệ độ tin cậy rõ nét dưới dạng phần trăm lớn.
   - So sánh trực quan các nhãn bệnh thay thế qua biểu đồ thanh tỉ lệ (Top-K predictions).
   - Tự động hiển thị cảnh cáo (cận kề) nếu khoảng cách tin cậy của top 1 và top 2 nhỏ hơn 10%.
   
3. **📚 Cơ sở tri thức (Knowledge Base)**:
   - Tra cứu trực tiếp danh sách bệnh được hệ thống hỗ trợ mà không cần chẩn đoán trước.
   - Xem chi tiết về triệu chứng bệnh, nguyên nhân, biện pháp điều trị, cách phòng ngừa và nguồn tài liệu tham khảo chính thức.
   
4. **📋 Lịch sử chẩn đoán cá nhân**:
   - Đăng ký và đăng nhập tài khoản người dùng (sử dụng Token JWT lưu trữ tại localStorage).
   - Tự động đồng bộ và lưu trữ lịch sử chẩn đoán khi người dùng đăng nhập.
   - Xem danh sách lịch sử phân trang trực quan kèm hình ảnh thu nhỏ.

---

## 🌐 Truy cập bản đã deploy

Ứng dụng hiện đã được deploy lên cloud và truy cập qua URL công khai:

- **Web App:** `https://plant-disease-demo.duckdns.org`
- **Backend API:** `https://plant-disease-demo.duckdns.org/api/v1`
- **Swagger UI:** `https://plant-disease-demo.duckdns.org/docs`

Frontend production cần build với biến môi trường:

```bash
NEXT_PUBLIC_API_BASE_URL=https://plant-disease-demo.duckdns.org/api/v1
```

## 🛠️ Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Cấu hình biến môi trường
Tạo file cấu hình `.env.local` từ file mẫu:
```bash
cp .env.example .env.local
```
Mặc định file mẫu đang trỏ tới API cloud: `https://plant-disease-demo.duckdns.org/api/v1`. Nếu cần chạy phát triển cục bộ, xem thêm hướng dẫn riêng tại `docs/DEVELOPMENT.md`.

### 2. Cài đặt thư viện
Chạy lệnh sau tại thư mục `frontend`:
```bash
npm install
```

### 3. Khởi chạy ứng dụng ở chế độ phát triển
```bash
npm run dev
```
Khi phát triển cục bộ, Next.js sẽ in URL dev server ra terminal sau khi chạy lệnh trên. Bản demo chính thức dùng URL cloud ở phần trên.

### 4. Build sản phẩm (Production)
Kiểm tra tính đúng đắn của kiểu dữ liệu và tối ưu hóa trước khi triển khai:
```bash
npm run build
```

### 5. Chạy Unit Test
Kiểm tra hoạt động của tầng giao tiếp API bằng Vitest:
```bash
npm run test
```

---

## ⚠️ Giới hạn kỹ thuật hiện tại
* **Segmentation Overlay**: Hiện tại ứng dụng chưa hỗ trợ vẽ đè vùng phát hiện bệnh (bounding box/segmentation mask) lên ảnh gốc do API Backend hiện hành chưa trả về tọa độ pixel hình học. Giao diện xem ảnh đã được thiết kế sẵn một vùng chứa (extension point) để dễ dàng tích hợp chức năng vẽ đè này khi Backend nâng cấp mô hình phân đoạn (ví dụ YOLO26-seg).
