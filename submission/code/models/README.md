# Tài liệu và Artifacts của Mô hình (Model Artifacts)

Thư mục này chứa các file cấu hình và thông tin của mô hình phục vụ cho việc chạy ứng dụng web.

## Hướng dẫn tải và thiết lập mô hình

1. **Liên kết tải file:**
   Truy cập liên kết Google Drive sau để tải các file mô hình và cấu hình cần thiết để chạy web: [Google Drive Folder](https://drive.google.com/drive/folders/1OS0M2uW8KuWymKMtZwIY8XMUGCBcBGwo?usp=sharing)

2. **Cách đặt file sau khi tải:**
   Hãy tải các file từ Google Drive và đặt vào đúng thư mục `ml-vietnam-plant-disease-detection/models/` trên máy của bạn.

   Các file cần có trong thư mục này bao gồm:
   - `yolo26_rice_quantized.onnx`: Mô hình YOLO26-seg lượng tử hóa (quantized) dạng ONNX cho Lúa.
   - `yolo26_coffee_quantized.onnx`: Mô hình YOLO26-seg lượng tử hóa (quantized) dạng ONNX cho Cà phê.
   - `class_names.json`: Danh sách nhãn tổng hợp của cả Lúa và Cà phê phục vụ suy luận.
   