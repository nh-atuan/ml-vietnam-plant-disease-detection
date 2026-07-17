# Dữ liệu Đồ án (Dataset Artifacts)

Thư mục này chứa thông tin hướng dẫn tải và cấu trúc tập dữ liệu phục vụ huấn luyện và đánh giá mô hình.

## Hướng dẫn tải dữ liệu

Do dung lượng tập dữ liệu rất lớn (~9.0 GB bao gồm ảnh gốc và nhãn phân vùng thực thể), toàn bộ dữ liệu đã được tải lên và lưu trữ trên Cloud.

1. **Liên kết tải dữ liệu:**
   Truy cập trang Kaggle sau để tải dữ liệu: [Kaggle Dataset - Rice & Coffee Leaf Disease](https://www.kaggle.com/datasets/magnusdtd2/rice-coffee-leaf-disease)

2. **Hướng dẫn thiết lập cục bộ:**
   Để chạy thử mã nguồn cục bộ hoặc chạy huấn luyện lại, hãy tải bộ dữ liệu từ Kaggle về và giải nén vào đúng thư mục gốc của dự án:
   ```text
   .
   └── data/
       ├── raw/
       │   ├── coffee_leaf_disease/
       │   └── rice_leaf_disease/
       └── processed/
           ├── images/
           └── metadata/
   ```

## Mô tả cấu trúc dữ liệu

* **data/raw/**: Dữ liệu thô ban đầu được thu thập từ nguồn crawl và chụp thực tế trên đồng ruộng.
  * `coffee_leaf_disease/`: Tập ảnh về các bệnh trên lá cà phê (Rỉ sắt, Nấm hồng, Sâu vẽ bùa, Tảo lục) kèm file chú thích định dạng COCO JSON.
  * `rice_leaf_disease/`: Tập ảnh về các bệnh trên lá lúa (Đạo ôn, Tiêm cánh, Đốm nâu, Khỏe mạnh) kèm file chú thích định dạng COCO JSON.
* **data/processed/**: Dữ liệu sau khi qua pipeline tiền xử lý, chuẩn hóa kích thước, phân chia tập Train/Val/Test và sẵn sàng đưa vào huấn luyện mô hình.

---

## Cách sinh dữ liệu tiền xử lý (data/processed/)

Dữ liệu tiền xử lý trong thư mục `data/processed/` được tạo ra tự động từ dữ liệu thô `data/raw/` bằng cách chạy pipeline được lập trình sẵn của nhóm.

Các bước thực hiện chi tiết:

1. **Cài đặt môi trường:**
   - Đảm bảo bạn đã cài đặt các thư viện phụ thuộc bằng công cụ `uv` tại thư mục `code/`:
     ```bash
     uv sync
     ```

2. **Chạy Pipeline Tiền xử lý:**
   - Mở và chạy tuần tự toàn bộ các cell trong Notebook tiền xử lý: [02_preprocessing.ipynb](file:///d:/HỌC KÌ 6/NHẬP MÔN HỌC MÁY/ĐỒ ÁN CUỐI KỲ/ml-vietnam-plant-disease-detection/submission/code/notebooks/02_preprocessing.ipynb) (nằm tại thư mục `code/notebooks/02_preprocessing.ipynb`).

3. **Chi tiết luồng xử lý tự động của Pipeline:**
   - **Lọc trùng lặp & Ảnh lỗi**: Pipeline sử dụng MD5 checksum để quét và tự động loại bỏ các ảnh trùng lặp hoặc các tệp tin ảnh bị lỗi định dạng vật lý.
   - **Phân chia tập dữ liệu (Splitting)**: Phân chia tập dữ liệu theo tỷ lệ chuẩn `70% Train / 15% Validation / 15% Test`. Pipeline áp dụng thuật toán chia ngẫu nhiên có kiểm soát để đảm bảo không xảy ra hiện tượng rò rỉ dữ liệu (data leakage) giữa các tập.
   - **Chuẩn hóa ảnh (Standardization)**: Resize ảnh gốc về kích thước pixel chuẩn, áp dụng kỹ thuật padding giữ nguyên tỷ lệ gốc của ảnh (letterbox padding) nhằm tránh biến dạng ảnh, đồng thời thực hiện chuẩn hóa pixel (pixel normalization).
   - **Xuất kết quả**:
     - Lưu ảnh đã chuẩn hóa vào `data/processed/images/` theo cấu trúc phân cấp: `train/`, `val/`, `test/` tiếp đến là loại cây (`coffee`/`rice`) và nhãn bệnh tương ứng.
     - Xuất các tệp manifest và thông tin cấu hình phân phối vào `data/processed/metadata/` dưới dạng các file `.csv` và `.json` (chứa các thông số như mean, std và danh sách ảnh thuộc từng split).
