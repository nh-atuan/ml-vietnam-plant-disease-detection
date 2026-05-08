# ĐẠI HỌC QUỐC GIA TPHCM
## TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN
### KHOA CÔNG NGHỆ THÔNG TIN

---

# ĐỀ CƯƠNG SƠ BỘ

**Đề tài: Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp đặc sản (Cà phê/Lúa) hỗ trợ nông dân**

**Môn học: CSC14005 - Nhập môn học máy**

*Sinh viên thực hiện:*
- Nguyễn Hồ Anh Tuấn - 23120185
- Lê Xuân Trí - 23120099
- Đàm Tiến Đạt - 23120118
- Tống Thanh Phúc - 23120158
- Dương Tuấn Anh - 23120208

*Giáo viên hướng dẫn:*
Thầy Bùi Tiến Lên

Ngày 30 tháng 3 năm 2026

---

## Mục lục

1. [Giới thiệu và động lực nghiên cứu](#1-giới-thiệu-và-động-lực-nghiên-cứu)
2. [Phát biểu bài toán](#2-phát-biểu-bài-toán)
3. [Thu thập và chuẩn bị dữ liệu](#3-thu-thập-và-chuẩn-bị-dữ-liệu)
   - 3.1 Nguồn dữ liệu
   - 3.2 Pipeline chuẩn bị dữ liệu
4. [Tiền xử lý và phân tích khám phá](#4-tiền-xử-lý-và-phân-tích-khám-phá)
   - 4.1 Kế hoạch tiền xử lý dự kiến
   - 4.2 Kế hoạch EDA dự kiến
5. [Lựa chọn và huấn luyện mô hình](#5-lựa-chọn-và-huấn-luyện-mô-hình)
6. [Đánh giá và tinh chỉnh mô hình](#6-đánh-giá-và-tinh-chỉnh-mô-hình)
   - 6.1 Chiến lược đánh giá
   - 6.2 Baseline, tuning và phân tích lỗi
   - 6.3 Quy trình cải thiện mô hình
   - 6.4 Tiêu chí chọn mô hình cuối cùng
7. [Xây dựng ứng dụng và triển khai demo](#7-xây-dựng-ứng-dụng-và-triển-khai-demo)
   - 7.1 Phạm vi ứng dụng
   - 7.2 Kiến trúc
   - 7.3 Kết quả kỳ vọng
8. [Kế hoạch triển khai & demo sản phẩm](#8-kế-hoạch-triển-khai--demo-sản-phẩm)
   - 8.1 Mục tiêu triển khai
   - 8.2 Pipeline triển khai tổng thể
   - 8.3 Công nghệ triển khai
9. [Kế hoạch thực hiện, rủi ro và hướng giảm thiểu](#9-kế-hoạch-thực-hiện-rủi-ro-và-hướng-giảm-thiểu)
   - 9.1 Tiến độ theo mốc học phần
   - 9.2 Rủi ro chính và phương án xử lý
   - 9.3 Sản phẩm bàn giao dự kiến

---

## 1 Giới thiệu và động lực nghiên cứu

Sản xuất lúa gạo và cà phê đóng vai trò quan trọng trong nông nghiệp Việt Nam, nhưng năng suất thường bị ảnh hưởng mạnh bởi bệnh lá và sâu bệnh phát sinh theo mùa. Trong thực tế, nhiều hộ nông dân chưa tiếp cận được chuyên gia bệnh học cây trồng kịp thời, dẫn đến chẩn đoán muộn và xử lý chưa đúng cách.

Đề tài hướng tới xây dựng một hệ thống học máy hỗ trợ nông dân nhận diện bệnh trên lá cây từ ảnh chụp điện thoại, từ đó cung cấp kết quả chẩn đoán nhanh và nhất quán. Mục tiêu học thuật là triển khai đầy đủ quy trình end-to-end theo yêu cầu môn học: từ phát biểu bài toán, chuẩn bị dữ liệu, huấn luyện mô hình, đánh giá, đến tích hợp thành ứng dụng web có khả năng demo công khai.

Ngoài giá trị ứng dụng, đề tài còn tạo cơ sở để phân tích các thách thức điển hình của thị giác máy tính trong nông nghiệp như nhiễu điều kiện chụp, mất cân bằng lớp bệnh, và sự tương đồng hình thái giữa các bệnh khác nhau.

---

## 2 Phát biểu bài toán

Mô hình hóa bài toán dưới dạng phân loại ảnh đa lớp (multi-class image classification).

**Input:** Ảnh RGB của lá cây (lúa hoặc cà phê), ký hiệu x ∈ R^(H×W×3).

**Output:** Nhãn bệnh y ∈ Y, trong đó Y bao gồm lớp healthy và các lớp bệnh phổ biến sau khi chuẩn hóa nhãn liên nguồn.

**Mục tiêu học máy:** Học hàm phân loại f_θ : x → y sao cho tối ưu hóa macro F1-score trên tập kiểm thử và duy trì thời gian suy luận phù hợp để triển khai web.

**Các thách thức chính:**

- Độ tương đồng cao giữa các bệnh ở giai đoạn sớm.
- Biến thiên lớn trong cùng một lớp do điều kiện ánh sáng, góc chụp, nền ảnh.
- Mất cân bằng nhãn giữa các lớp bệnh và giữa hai nhóm cây trồng.
- Nhiễu dữ liệu thực tế: ảnh mờ, che khuất, hoặc chứa nhiều lá trong cùng khung hình.

**Mục tiêu thực tiễn:** Xây dựng và triển khai thành công một hệ thống AI chẩn đoán bệnh cây trồng đạt độ chính xác cao, vận hành ổn định trên môi trường microservices.

---

## 3 Thu thập và chuẩn bị dữ liệu

### 3.1 Nguồn dữ liệu

Kết hợp nhiều nguồn dữ liệu mở nhằm tăng độ đa dạng về điều kiện chụp, giống cây trồng và biểu hiện bệnh, từ đó giúp mô hình có khả năng tổng quát hóa tốt hơn trong môi trường thực tế.

Các bộ dữ liệu chính được sử dụng bao gồm:

- **Rice Diseases Image Dataset (Việt Nam)**
  Link: kaggle.com/datasets/minhhuy2810/rice-diseases-image-dataset
  Dataset gồm hơn 3.300 ảnh lá lúa được thu thập tại Việt Nam, chia thành 4 lớp: 1 lớp Healthy cho những cây khỏe mạnh, Brown Spot và 3 lớp cho cây nhiễm bệnh Leaf Blast, Leaf Roller.

- **Rice Leaf Disease and Pest Dataset (Mendeley)**
  Link: data.mendeley.com/datasets/c5yvn32dzg/2
  Dataset gồm 2.769 ảnh gốc và được mở rộng lên hơn 19.000 ảnh thông qua augmentation. Bộ dữ liệu này cung cấp sự đa dạng về điều kiện môi trường và loại bệnh.

- **Rice Leaf Bacterial and Fungal Disease Dataset (Mendeley)**
  Link: data.mendeley.com/datasets/vwv3nry3wr/1
  Dataset gồm 1.701 ảnh gốc (và hơn 5.000 ảnh augmented), tập trung vào các bệnh do vi khuẩn và nấm trên lúa. Bộ dữ liệu giúp bổ sung các lớp bệnh chuyên biệt mà các dataset khác chưa bao phủ.

- **RoCoLe – Robusta Coffee Leaf Dataset (Mendeley)**
  Link: data.mendeley.com/datasets/hx6f852hw4/2
  Dataset gồm 1.560 ảnh độ phân giải cao của lá cà phê Robusta, với nhãn chi tiết về bệnh như rỉ sắt (nhiều mức độ) và nhện đỏ. Đây là bộ dữ liệu chính cho nhánh cà phê trong bài toán.

**Tích hợp dữ liệu.** Do dữ liệu đến từ nhiều nguồn khác nhau, nhóm áp dụng các bước chuẩn hóa sau:

- **Chuẩn hóa nhãn:** Xây dựng taxonomy chung, gom các nhãn tương đương giữa các dataset (ví dụ: các biến thể của leaf blast).
- **Tách domain theo loại cây:** Phân biệt rõ hai domain lúa và cà phê, đồng thời đảm bảo mỗi domain có đủ số lượng mẫu cho huấn luyện.
- **Loại bỏ trùng lặp và nhiễu:** Áp dụng hash-based duplicate detection kết hợp kiểm tra thủ công.
- **Kiểm soát mất cân bằng dữ liệu:** Theo dõi phân phối lớp ngay từ bước hợp nhất để phục vụ weighting và augmentation ở các bước sau.

Sau khi hợp nhất và làm sạch, quy mô dữ liệu kỳ vọng đạt khoảng 10.000–15.000 ảnh, bao gồm cả ảnh gốc và ảnh được tăng cường dữ liệu.

### 3.2 Pipeline chuẩn bị dữ liệu

1. Hợp nhất metadata và kiểm tra định dạng ảnh.
2. Loại ảnh trùng lặp và ảnh lỗi (hash-based duplicate check + kiểm tra thủ công).
3. Chuẩn hóa nhãn liên nguồn theo taxonomy thống nhất.
4. Tách tập dữ liệu theo tỷ lệ Train 70% – Validation 15% – Test 15% bằng stratified split.
5. Chỉ áp dụng augmentation sau khi đã chia dữ liệu để tránh gây rò rỉ dữ liệu.

Sau khi có dữ liệu sạch và nhất quán, nhóm sẽ tiến hành phân tích khám phá để hiểu đặc tính dữ liệu trước khi huấn luyện.

---

## 4 Tiền xử lý và phân tích khám phá

### 4.1 Kế hoạch tiền xử lý dự kiến

Pipeline tiền xử lý thống nhất cho toàn bộ ảnh gồm:

- Resize về kích thước chuẩn và chuẩn hóa giá trị pixel.
- Chuẩn hóa không gian màu, loại ảnh bị hỏng hoặc quá mờ.
- Augmentation trên tập train: random flip/rotation, color jitter, cutout, mixup,...

### 4.2 Kế hoạch EDA dự kiến

Thực hiện các phân tích sau:

- **Class distribution:** biểu đồ phân phối số mẫu theo lớp bệnh để phát hiện mất cân bằng.
- **Sample visualization:** hiển thị ảnh đại diện cho từng lớp để kiểm tra chất lượng nhãn.
- **Resolution & quality distribution:** thống kê độ phân giải, độ sáng, độ mờ.
- **Disease similarity inspection:** phân nhóm các cặp bệnh dễ nhầm lẫn theo đặc trưng hình thái.

Kết quả EDA sẽ được dùng để điều chỉnh chiến lược augmentation, weighting theo lớp và thiết kế tiêu chí đánh giá phù hợp.

---

## 5 Lựa chọn và huấn luyện mô hình

Thử nghiệm tối thiểu ba mô hình theo yêu cầu môn học, đồng thời mở rộng so sánh để cân bằng giữa độ chính xác và khả năng triển khai thực tế.

**Bảng 1: Các mô hình dự kiến và vai trò trong thực nghiệm**

| Mô hình | Vai trò |
|---|---|
| MobileNetV2 | Baseline nhẹ, tốc độ suy luận nhanh, phù hợp thiết bị tài nguyên hạn chế. |
| ResNet50 | CNN chuẩn mạnh để so sánh chất lượng biểu diễn đặc trưng. |
| Swin Transformer | Mô hình transformer thị giác, kỳ vọng cải thiện độ chính xác ở mẫu khó. |
| DINOv3 (fine-tune) | Khai thác biểu diễn tự giám sát để tăng khả năng tổng quát hóa. |

**Thiết lập huấn luyện dự kiến:**

- Transfer learning từ pretrained weights.
- Tối ưu bằng AdamW, learning-rate scheduler và early stopping theo macro F1 trên validation.
- So sánh thêm các chỉ số thực dụng: thời gian train, thời gian inference và kích thước mô hình.

Phần mô hình tốt nhất sẽ không chỉ dựa trên accuracy cao nhất mà dựa trên đánh đổi giữa hiệu năng và tính khả thi khi triển khai ứng dụng cho người dùng cuối. Dựa trên thiết kế huấn luyện này, phần tiếp theo mô tả chiến lược đánh giá và tinh chỉnh chi tiết.

---

## 6 Đánh giá và tinh chỉnh mô hình

### 6.1 Chiến lược đánh giá

**(1) Thiết kế đánh giá chuẩn hóa.** Giữ chiến lược chia tập có phân tầng đã nêu ở Mục 3, gồm train, validation và test cố định, nhằm bảo đảm so sánh công bằng giữa các kiến trúc.

- Validation set chỉ dùng cho tuning và chọn checkpoint.
- Test set cố định được khóa đến cuối quy trình, không dùng trong quá trình dò tham số.
- Báo cáo kết quả ở cả hai mức: toàn bộ dữ liệu và theo từng domain (lúa, cà phê) để kiểm tra khả năng tổng quát hóa khi có domain shift.
- Bổ sung robustness check bằng các nhiễu nhẹ ở thời điểm đánh giá (thay đổi sáng tối nhẹ, blur nhẹ, thay đổi tương phản mức nhỏ) để đo độ bền của mô hình trước dữ liệu thực địa.

**(2) Bộ metrics mở rộng.** Thay vì chỉ dựa vào một chỉ số đơn lẻ, nhóm đánh giá theo ba tầng chỉ số:

- **Core metrics:** Macro F1-score (metric chính), Weighted F1-score (bổ sung khi mất cân bằng lớp mạnh), Accuracy.
- **Class-level metrics:** Precision/Recall/F1 theo từng lớp, kèm support để tránh diễn giải sai ở các lớp ít mẫu.
- **System-level metrics:** thời gian suy luận trung bình (ms/ảnh), kích thước mô hình (MB), và thông lượng suy luận (ảnh/giây) khi cần so sánh phục vụ triển khai.

**(3) Trực quan hóa kết quả.** Để tăng chiều sâu phân tích, các biểu đồ được báo cáo đồng bộ gồm:

- Confusion matrix dạng đếm tuyệt đối và dạng chuẩn hóa theo hàng.
- Đường học theo epoch (train/validation loss, macro F1) để quan sát overfitting.
- ROC dạng one-vs-rest cho các lớp chính (khi số mẫu lớp đủ lớn).

### 6.2 Baseline, tuning và phân tích lỗi

**(1) Thiết lập baseline rõ ràng.** Theo định hướng ở Mục 5, nhóm dùng hai baseline chuẩn để tạo mốc so sánh:

- **Baseline 1 – MobileNetV2:** huấn luyện theo cấu hình chuẩn, không tuning sâu; đại diện cho nhánh nhẹ, ưu tiên tốc độ.
- **Baseline 2 – ResNet50:** huấn luyện theo cấu hình chuẩn; đại diện cho CNN sâu làm chuẩn chất lượng đặc trưng.

Các mô hình còn lại (Swin Transformer, DINOv3 fine-tune, YOLO-cls) được xem là ứng viên cải thiện sau baseline.

**(2) Hyperparameter tuning theo pipeline có kiểm soát.** Quy trình tuning được triển khai theo hai pha để cân bằng chi phí tính toán và độ bao phủ không gian tham số:

- **Pha 1 (thăm dò nhanh):** random search trong không gian hẹp để xác định vùng tham số tiềm năng.
- **Pha 2 (tinh chỉnh):** mở rộng trial bằng Ray Tune cho các mô hình có triển vọng cao.

**Bảng 2: Không gian siêu tham số chính cho tuning**

| Siêu tham số | Khoảng tìm kiếm đề xuất |
|---|---|
| Learning rate | 10^-5 đến 10^-3 (log scale) |
| Batch size | {16, 32, 64} |
| Weight decay | 10^-5 đến 10^-2 |
| Dropout (nếu kiến trúc hỗ trợ) | 0.0 đến 0.5 |
| Mức augmentation | yếu/trung bình/mạnh theo cùng pipeline dữ liệu |

Tất cả trial đều được theo dõi bằng MLflow (tham số, metric theo epoch, artifact như confusion matrix và checkpoint) để đảm bảo khả năng truy vết và tái lập thực nghiệm.

**(3) Error analysis theo nhóm lỗi.** Error analysis là trọng tâm để tạo vòng lặp cải thiện thay vì dừng ở báo cáo metric:

- **Nhóm 1 – visual similarity:** các cặp bệnh có triệu chứng gần giống nhau.
- **Nhóm 2 – chất lượng ảnh thấp:** ảnh mờ, thiếu sáng, nhiễu nền mạnh.
- **Nhóm 3 – bố cục phức tạp:** ảnh chứa nhiều lá hoặc bị che khuất.
- **Nhóm 4 – healthy vs early disease:** nhầm lẫn giữa lá khỏe và giai đoạn bệnh sớm.

Ưu tiên kiểm tra top-K dự đoán sai có confidence cao để phát hiện lỗi hệ thống dễ bị bỏ sót khi chỉ nhìn điểm số tổng.

**(4) Fine-grained analysis.** Ngoài phân tích tổng thể, nhóm báo cáo thêm:

- F1 theo từng lớp để xác định lớp yếu cần xử lý bổ sung dữ liệu hoặc augmentation mục tiêu.
- Hiệu năng theo từng domain (rice-only, coffee-only) để đánh giá độ ổn định liên miền.
- Calibration (ví dụ reliability diagram, ECE/Brier score) để kiểm tra độ tin cậy của confidence trước khi đưa vào ứng dụng ở Mục 7.

### 6.3 Quy trình cải thiện mô hình

Để đáp ứng yêu cầu phân tích sâu của học phần, nhóm áp dụng quy trình lặp **Evaluate → Analyze → Improve → Re-evaluate:**

1. Huấn luyện baseline theo cấu hình chuẩn.
2. Đánh giá trên validation bằng bộ metric chuẩn hóa.
3. Phân tích lỗi theo confusion matrix, nhóm lỗi và top-K sai confidence cao.
4. Áp dụng can thiệp mục tiêu (tuning augmentation, class weighting, fine-tune sâu hơn, hoặc đổi kiến trúc).
5. Huấn luyện lại với cấu hình cập nhật.
6. Đánh giá lại và so sánh với vòng trước bằng cùng protocol.

Quy trình này được lặp cho đến khi cải thiện hội tụ hoặc đạt ngưỡng tài nguyên/thời gian đã đặt ra.

### 6.4 Tiêu chí chọn mô hình cuối cùng

Mô hình cuối để triển khai không được chọn theo một chỉ số duy nhất mà theo tiêu chí đa mục tiêu:

- **Hiệu năng dự đoán:** ưu tiên Macro F1 cao và ổn định trên test set cố định.
- **Độ ổn định học:** khoảng cách train–validation hợp lý, không overfit nghiêm trọng.
- **Chi phí suy luận:** thời gian suy luận và thông lượng phù hợp mục tiêu phục vụ web.
- **Tính triển khai:** kích thước mô hình, bộ nhớ sử dụng và khả năng chuyển đổi ONNX.
- **Độ tin cậy dự đoán:** confidence được hiệu chỉnh tốt để hỗ trợ diễn giải kết quả cho người dùng cuối.

---

## 7 Xây dựng ứng dụng và triển khai demo

### 7.1 Phạm vi ứng dụng

Ứng dụng web cho phép người dùng tải ảnh lá cây, hệ thống trả về:

- Lớp bệnh dự đoán và độ tin cậy.
- Top-k nhãn có xác suất cao.
- Gợi ý xử lý ban đầu theo luật chuyên gia ở mức tham khảo.

### 7.2 Kiến trúc

Các kiến trúc & công nghệ triển khai dự kiến bao gồm:

- **Frontend:** Next.js kết hợp Tailwind CSS.
- **Backend:** FastAPI, sử dụng mô hình từ MLflow Model Registry để thực hiện inference qua REST API.
- **PostgreSQL:** Lưu metadata của ảnh, kết quả của model.
- **MinIO:** Hoạt động giống S3 của AWS, dùng để lưu trữ ảnh.
- **Redis:** Dùng để lưu trữ kết quả tạm thời, giúp tăng tốc việc truy xuất.

### 7.3 Kết quả kỳ vọng

- Mô hình phân loại bệnh đạt macro F1 cao và ổn định trên tập test.
- Ứng dụng web chạy ổn định, có URL công khai để demo.
- Báo cáo phân tích ưu/nhược điểm mô hình dựa trên kết quả thực nghiệm.

---

## 8 Kế hoạch triển khai & demo sản phẩm

### 8.1 Mục tiêu triển khai

Mục tiêu của giai đoạn triển khai là chuyển mô hình đã huấn luyện thành một dịch vụ có thể sử dụng bởi người dùng cuối trong điều kiện gần thời gian thực.

- Cung cấp hệ thống có thể truy cập qua URL công khai để phục vụ cho phần demo.
- Đảm bảo thời gian phản hồi ổn định ở mức real-time hoặc near real-time cho truy vấn ảnh đơn lẻ.
- Duy trì khả năng mở rộng theo tải truy cập và có cơ chế theo dõi vận hành liên tục.

Phần này liên kết trực tiếp mục tiêu học máy với mục tiêu của môn học về xây dựng hệ thống ML end-to-end.

### 8.2 Pipeline triển khai tổng thể

Luồng triển khai chính: **Training → Model selection → Export → Serving → Web → User.**

Pipeline được tổ chức theo các bước sau:

1. Huấn luyện các mô hình phân loại bằng PyTorch trên tập dữ liệu đã chuẩn hóa.
2. Chọn mô hình tốt nhất theo tiêu chí đa mục tiêu, trọng tâm là macro F1 và chi phí suy luận.
3. Chuyển đổi mô hình đã chọn sang định dạng ONNX để chuẩn hóa khâu phục vụ suy luận.
4. Đăng ký phiên bản mô hình vào MLflow Model Registry để quản lý vòng đời mô hình.
5. Triển khai dịch vụ suy luận qua FastAPI dưới dạng REST API.
6. Tích hợp frontend để gọi API và hiển thị kết quả dự đoán cho người dùng.

### 8.3 Công nghệ triển khai

**Bảng 3: DevOps & MLOps stack và vai trò**

| Thành phần | Vai trò trong hệ thống |
|---|---|
| Docker | Đóng gói frontend, backend và dịch vụ phụ trợ thành các container độc lập, dễ tái lập môi trường. |
| Kubernetes (k8s) | Điều phối container, mở rộng dịch vụ, tự phục hồi khi pod gặp lỗi. |
| ONNX | Chuẩn hóa mô hình để tối ưu thời gian suy luận và tăng tính tương thích khi triển khai. |
| GitHub Actions | Tự động hóa CI/CD: kiểm tra, build image và triển khai bản cập nhật. |
| Traefik | Reverse proxy, định tuyến request và quản lý truy cập vào các dịch vụ nội bộ. |
| DuckDNS | Cung cấp tên miền động để công khai URL demo trong điều kiện hạ tầng giới hạn. |

---

## 9 Kế hoạch thực hiện, rủi ro và hướng giảm thiểu

### 9.1 Tiến độ theo mốc học phần

**Bảng 4: Kế hoạch triển khai theo tuần**

| Giai đoạn | Công việc chính |
|---|---|
| Tuần 3–6 | Thu thập và hợp nhất dữ liệu, chuẩn hóa nhãn, hoàn thành EDA ban đầu, chốt pipeline tiền xử lý. |
| Tuần 6–10 | Huấn luyện và so sánh các mô hình, tuning tham số, phân tích lỗi, chọn mô hình tốt nhất theo macro F1 và chi phí suy luận. |
| Tuần 10–báo cáo cuối kỳ | Tích hợp mô hình vào FastAPI, hoàn thiện giao diện web, deploy Docker lên cloud công khai, viết báo cáo và chuẩn bị slide bảo vệ. |

### 9.2 Rủi ro chính và phương án xử lý

- **Mất cân bằng dữ liệu:** dùng class weighting, augmentation có kiểm soát và đánh giá bằng macro F1.
- **Domain shift giữa các nguồn ảnh:** kiểm tra phân bố theo nguồn, bổ sung ảnh thực địa và theo dõi hiệu năng theo từng miền dữ liệu.
- **Quá tải phạm vi kỹ thuật:** ưu tiên mục tiêu học máy và demo chạy ổn định trước khi mở rộng tính năng.
- **Rủi ro tiến độ:** chia milestone nhỏ theo tuần, review nội bộ định kỳ để phát hiện sớm vấn đề.

### 9.3 Sản phẩm bàn giao dự kiến

- Báo cáo khoa học theo đầy đủ 7 bước quy trình của môn.
- Mã nguồn huấn luyện, đánh giá và ứng dụng web.
