# TÀI LIỆU KHẢO SÁT & ĐẶC TẢ API (API DOCUMENTATION)

Hệ thống API Backend được xây dựng bằng **FastAPI** cung cấp các dịch vụ chẩn đoán bệnh lá cây, tra cứu cơ sở tri thức chuyên gia, lưu trữ lịch sử chẩn đoán và quản lý tài khoản người dùng.

---

## 1. TRUY CẬP ĐƯỜNG DẪN TÀI LIỆU TỰ ĐỘNG

Backend hiện đã được deploy lên cloud. Bạn có thể truy cập tài liệu API dạng tương tác động tại:
*   **Swagger UI:** `https://plant-disease-demo.duckdns.org/docs` (Giao diện thử nghiệm trực tiếp).
*   **ReDoc:** `https://plant-disease-demo.duckdns.org/redoc` (Giao diện đọc tài liệu chuyên sâu).
*   **API base URL:** `https://plant-disease-demo.duckdns.org/api/v1`

File đặc tả OpenAPI Spec (JSON) tĩnh được lưu tại:
*   [openapi.json](./openapi.json)

---

## 2. CHI TIẾT CÁC ENDPOINTS

### 2.1. HỆ TRI THỨC CHUYÊN GIA (KNOWLEDGE)

#### 2.1.1. Lấy danh sách bệnh hỗ trợ
*   **Path:** `/api/v1/knowledge`
*   **Method:** `GET`
*   **Mô tả:** Lấy danh sách toàn bộ các nhãn bệnh (kèm thông tin cây trồng, tên tiếng Việt, tên tiếng Anh, mức độ nguy hiểm) có trong cơ sở tri thức.
*   **Response mẫu (`200 OK`):**
    ```json
    {
      "items": [
        {
          "label": "AlgalLeafSpot",
          "crop": "coffee",
          "name_vi": "Bệnh đốm rong trên cà phê",
          "name_en": "Algal Leaf Spot",
          "severity": "medium"
        },
        {
          "label": "BrownSpot",
          "crop": "rice",
          "name_vi": "Bệnh đốm nâu hại lúa",
          "name_en": "Brown Spot",
          "severity": "medium"
        }
      ],
      "total": 8
    }
    ```

#### 2.1.2. Lấy thông tin chi tiết của một bệnh
*   **Path:** `/api/v1/knowledge/{disease_label}`
*   **Method:** `GET`
*   **Tham số đường dẫn (Path Parameter):**
    *   `disease_label` (string, bắt buộc): Nhãn mô hình (ví dụ: `Rust`, `LeafBlast`, `Healthy`).
*   **Mô tả:** Trả về toàn bộ thông tin chi tiết về triệu chứng, nguyên nhân, cách xử lý, biện pháp phòng bệnh và nguồn tài liệu tham khảo chính thống của bệnh được yêu cầu.
*   **Response mẫu (`200 OK`):**
    ```json
    {
      "label": "Rust",
      "crop": "coffee",
      "name_vi": "Bệnh gỉ sắt cà phê",
      "name_en": "Rust",
      "description": "Bệnh gỉ sắt cà phê là bệnh quan trọng trên lá...",
      "symptoms": [
        "Mặt dưới lá có ổ bột màu vàng cam giống gỉ sắt.",
        "Mặt trên lá có đốm vàng tương ứng với vị trí ổ bệnh."
      ],
      "causes": [
        "Nấm gỉ sắt phát tán bào tử qua gió, nước mưa..."
      ],
      "treatments": [
        "Thu gom lá rụng bệnh nặng dưới tán để giảm nguồn bào tử.",
        "Tỉa cành tạo tán thông thoáng, giảm ẩm trong vườn."
      ],
      "prevention": [
        "Trồng hoặc cải tạo bằng giống có khả năng chống chịu..."
      ],
      "severity": "high",
      "sources": [
        {
          "title": "CABI PlantwisePlus Knowledge Bank",
          "url": "https://plantwiseplusknowledgebank.org/"
        }
      ]
    }
    ```
*   **Phản hồi lỗi thường gặp:**
    *   `404 Not Found`: Khi `disease_label` không tồn tại trong cơ sở dữ liệu.
        ```json
        { "detail": "Unknown disease label: InvalidLabel" }
        ```

---

### 2.2. CHẨN ĐOÁN HÌNH ẢNH (PREDICT)

#### 2.2.1. Gửi ảnh lá cây chẩn đoán bệnh
*   **Path:** `/api/v1/predict`
*   **Method:** `POST`
*   **Content-Type:** `multipart/form-data`
*   **Body (Form Data):**
    *   `file` (file bytes, bắt buộc): Ảnh chụp lá cây lúa hoặc cà phê dưới định dạng `.jpg`, `.jpeg`, `.png` hoặc `.webp`. Dung lượng tối đa là 10 MB.
*   **Mô tả:** Upload ảnh lá cây lên hệ thống, chạy mô hình phân đoạn YOLO26-seg để nhận diện và khoanh vùng bệnh trên lá, lưu trữ ảnh vào kho MinIO, lưu bản ghi vào DB, đồng thời đính kèm gợi ý xử lý tương ứng từ Expert Knowledge Base.
*   **Response mẫu (`200 OK` - Khi tích hợp xong Model Serving):**
    ```json
    {
      "prediction": "BrownSpot",
      "confidence": 0.92,
      "top_k": [
        { "label": "BrownSpot", "confidence": 0.92 },
        { "label": "LeafBlast", "confidence": 0.05 },
        { "label": "Healthy", "confidence": 0.03 }
      ],
      "recommendation": {
        "label": "BrownSpot",
        "crop": "rice",
        "name_vi": "Bệnh đốm nâu hại lúa",
        "name_en": "Brown Spot",
        "description": "Bệnh đốm nâu trên lúa thường tạo các vết nâu hình tròn...",
        "symptoms": [...],
        "causes": [...],
        "treatments": [...],
        "prevention": [...],
        "severity": "medium",
        "confidence": 0.92,
        "confidence_note": "Kết quả có độ tin cậy tương đối; cần đối chiếu với triệu chứng thực tế trên ruộng hoặc vườn.",
        "advisory": "Khuyến nghị chỉ mang tính tham khảo..."
      },
      "image_id": "d3b07384-d113-4ec3-a558-ee2b1154c123",
      "image_url": "https://plant-disease-demo.duckdns.org/plant-disease/images/d3b07384.jpg?X-Amz-Signature=..."
    }
    ```
*   **Phản hồi lỗi thường gặp:**
    *   `400 Bad Request`: Ảnh tải lên trống rỗng.
    *   `413 Payload Too Large`: Ảnh vượt quá giới hạn 10 MB.
    *   `415 Unsupported Media Type`: Ảnh sai định dạng (ví dụ gửi file text, pdf...).
    *   `503 Service Unavailable`: Dịch vụ suy luận mô hình chưa cấu hình hoàn thiện.

---

### 2.3. CÁC ENDPOINT DỰ KIẾN TRIỂN KHAI (PLANNED ENDPOINTS - PHASE 5.2 & 5.3)

Các endpoint dưới đây được thiết kế khung Schema sẵn sàng để thành viên phụ trách Backend phát triển router kết nối với tầng Database CRUD hiện tại:

#### 2.3.1. Đăng ký tài khoản (`POST /api/v1/auth/register`)
*   **Body (JSON):**
    ```json
    {
      "username": "farmer_john",
      "email": "john@example.com",
      "password": "secretpassword123"
    }
    ```
*   **Response mẫu (`200 OK`):** Trả về thông tin người dùng được tạo (đã băm mật khẩu bảo mật).
    ```json
    {
      "id": "e4f890c2-3cf1-4a4f-9e67-8fd4a942b012",
      "username": "farmer_john",
      "email": "john@example.com",
      "is_active": true,
      "created_at": "2026-06-28T13:12:00"
    }
    ```

#### 2.3.2. Đăng nhập (`POST /api/v1/auth/login`)
*   **Body (JSON):**
    ```json
    {
      "username": "farmer_john",
      "password": "secretpassword123"
    }
    ```
*   **Response mẫu (`200 OK`):** Trả về mã Token truy cập để gắn vào Header `Authorization: Bearer <token>`.
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer"
    }
    ```

#### 2.3.3. Xem lịch sử chẩn đoán bệnh (`GET /api/v1/history`)
*   **Headers:** `Authorization: Bearer <token>`
*   **Tham số truy vấn (Query Parameters):**
    *   `page` (int, default=1)
    *   `page_size` (int, default=10)
*   **Response mẫu (`200 OK`):** Danh sách lịch sử phân trang gồm ảnh, nhãn dự đoán và khuyến nghị đi kèm.
    ```json
    {
      "items": [
        {
          "id": "784d852a-9fce-4279-88ff-c9179d612e4f",
          "image_id": "d3b07384-d113-4ec3-a558-ee2b1154c123",
          "predicted_label": "BrownSpot",
          "confidence": 0.92,
          "top_k": [
            { "label": "BrownSpot", "confidence": 0.92 }
          ],
          "recommendation": {
            "name_vi": "Bệnh đốm nâu hại lúa",
            "treatments": [...]
          },
          "image_url": "https://plant-disease-demo.duckdns.org/plant-disease/images/...",
          "created_at": "2026-06-28T13:15:30"
        }
      ],
      "total": 1,
      "page": 1,
      "page_size": 10
    }
    ```
