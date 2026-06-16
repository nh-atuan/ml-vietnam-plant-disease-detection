# ĐẠI HỌC QUỐC GIA TPHCM

## TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN

### KHOA CÔNG NGHỆ THÔNG TIN

---

# BÁO CÁO VỀ MÔ HÌNH

**Đề tài: Hệ thống phân vùng thực thể chẩn đoán bệnh trên lá cây nông nghiệp đặc sản cà phê và lúa**

---

**Môn học: CSC14005 - Nhập môn học máy**

*Sinh viên thực hiện:*
Nguyễn Hồ Anh Tuấn - 23120185
Lê Xuân Trí - 23120099
Đàm Tiến Đạt - 23120118
Tống Thanh Phúc - 23120158
Dương Tuấn Anh - 23120208

*Giáo viên hướng dẫn:*
Thầy Bùi Tiến Lên

Ngày 14 tháng 6 năm 2026

---

## Mục lục

- Danh sách bảng
- Danh sách hình vẽ
- Bảng thuật ngữ
- 1 Giới thiệu bài toán
  - 1.1 Phát biểu bài toán
    - 1.1.1 Định nghĩa hình thức
  - 1.2 Lý do chọn Instance Segmentation
- 2 Tổng quan dữ liệu đầu vào
  - 2.1 Nguồn và quy mô dữ liệu
  - 2.2 Phân chia dữ liệu và thiết lập chung
  - 2.3 Tiền xử lý ảnh
    - 2.3.1 Chuẩn hóa kích thước
    - 2.3.2 Xử lý dữ liệu mất cân bằng
    - 2.3.3 Tăng cường dữ liệu
- 3 Lựa chọn mô hình và kiến trúc
  - 3.1 Tổng quan các mô hình
  - 3.2 Mô hình 1: Mask R-CNN
    - 3.2.1 Lý do lựa chọn
    - 3.2.2 Kiến trúc chi tiết
    - 3.2.3 Hàm mất mát
  - 3.3 Mô hình 2: YOLO26m-seg
    - 3.3.1 Lý do lựa chọn
    - 3.3.2 Kiến trúc chi tiết
    - 3.3.3 Hàm mất mát
  - 3.4 Mô hình 3: RF-DETR
    - 3.4.1 Lý do lựa chọn
    - 3.4.2 Kiến trúc chi tiết
    - 3.4.3 Hàm mất mát
  - 3.5 Mô hình 4: MobileSAM
    - 3.5.1 Lý do lựa chọn
    - 3.5.2 Kiến trúc chi tiết
    - 3.5.3 Hàm mất mát
  - 3.6 Mô hình 5: Mask2Former
    - 3.6.1 Lý do lựa chọn
    - 3.6.2 Kiến trúc chi tiết
    - 3.6.3 Hàm mất mát
- 4 Cấu hình huấn luyện
  - 4.1 Thiết lập chung
  - 4.2 Tham số riêng theo mô hình
- 5 Kết quả thực nghiệm
  - 5.1 Biểu đồ quá trình học
  - 5.2 Đánh giá trên tập Test
  - 5.3 Confusion Matrix
  - 5.4 Phân tích lỗi và các trường hợp dự đoán sai
- 6 Thảo luận và lựa chọn mô hình
  - 6.1 So sánh tổng hợp các mô hình
  - 6.2 Lựa chọn mô hình triển khai
  - 6.3 Hyperparameter Tuning cho YOLO26m-seg
    - 6.3.1 Phương pháp: Ray Tune với ASHAScheduler
    - 6.3.2 Thiết lập thực nghiệm
    - 6.3.3 Kết quả tinh chỉnh
- 7 Kết luận
- Tài liệu tham khảo

---

## Danh sách bảng

1. Thống kê bộ dữ liệu sau tiền xử lý
2. Tỷ lệ phân chia tập dữ liệu
3. Các kỹ thuật tăng cường dữ liệu được sử dụng
4. Tổng quan 5 mô hình segmentation được lựa chọn
5. Thiết lập huấn luyện chung cho tất cả 5 mô hình
6. Tham số riêng của từng mô hình
7. Kết quả đánh giá 5 mô hình trên tập Test (Rice và Coffee)
8. Bảng so sánh đa tiêu chí giữa 5 mô hình phân vùng thực thể
9. Không gian tìm kiếm siêu tham số cho YOLO26m-seg
10. Kết quả YOLO26m-seg trước và sau khi tinh chỉnh siêu tham số

---

## Danh sách hình vẽ

1. Sơ đồ kiến trúc mô hình Mask R-CNN với backbone ResNet-50 FPN
2. Sơ đồ khối kiến trúc YOLO26m-seg sử dụng trong thực nghiệm
3. Sơ đồ luồng kiến trúc RF-DETR segmentation
4. Sơ đồ luồng kiến trúc MobileSAM áp dụng trong bài toán phân vùng.
5. Sơ đồ kiến trúc Mask2Former với backbone Swin-T.
6. Learning curves của 5 mô hình trên tập Lúa. Đường liền: validation loss; đường đứt: training loss.
7. Learning curves của 5 mô hình trên tập Cà phê. Đường liền: validation loss; đường đứt: training loss.
8. Confusion matrix của Mask R-CNN trên tập Test.
9. Confusion matrix của YOLO26m-seg trên tập Test.
10. Confusion matrix của RF-DETR trên tập Test.
11. Confusion matrix của MobileSAM trên tập Test.
12. Confusion matrix của Mask2Former trên tập Test.
13. Các ví dụ trực quan về dự đoán sai (ảnh gốc, nhãn thực tế Ground Truth và dự đoán của mô hình Mask R-CNN) trên tập dữ liệu Rice.

---

## Bảng thuật ngữ

| Thuật ngữ | Định nghĩa |
|---|---|
| Instance Segmentation | Phân vùng từng đối tượng riêng lẻ trong ảnh, trả về mask pixel-level và nhãn lớp cho mỗi instance. |
| mAP@50 | Mean Average Precision ở ngưỡng IoU = 0.50 - chỉ số đánh giá detection/segmentation phổ biến. |
| mAP@50:95 | mAP trung bình trên nhiều ngưỡng IoU từ 0.50 đến 0.95 (bước 0.05) - đánh giá nghiêm ngặt hơn. |
| mIoU | Mean Intersection over Union - trung bình tỷ lệ giao/hợp giữa predicted mask và ground truth mask. |
| Dice Score | 2·\|A∩B\|/(\|A\|+\|B\|) - tương tự IoU nhưng ít nhạy cảm hơn với imbalance. |
| FPN | Feature Pyramid Network - kết nối đặc trưng đa tỷ lệ trong CNN backbone. |
| ViT | Vision Transformer - kiến trúc attention-based thay thế CNN cho computer vision. |
| ASHA | Asynchronous Successive Halving Algorithm - thuật toán early-stopping cho hyperparameter search. |
| ONNX | Open Neural Network Exchange - định dạng model độc lập framework, tối ưu cho inference. |
| RPN | Region Proposal Network - mạng con trong Mask R-CNN đề xuất vùng ứng viên chứa đối tượng. |
| SAM | Segment Anything Model - mô hình segmentation tổng quát của Meta AI. |

---

## 1 Giới thiệu bài toán

Bệnh trên lá cây nông nghiệp là một trong những nguyên nhân chính gây tổn thất mùa màng ở Việt Nam, đặc biệt đối với hai cây trồng chủ lực là lúa (*Oryza sativa*) và cà phê (*Coffea* spp.). Việc phát hiện bệnh sớm và chính xác giúp nông dân đưa ra biện pháp xử lý kịp thời, giảm thiệt hại về năng suất và chi phí thuốc bảo vệ thực vật.

Tuy nhiên, chẩn đoán bệnh cây truyền thống đòi hỏi chuyên gia nông nghiệp - đội ngũ vốn thiếu hụt ở các vùng nông thôn. Do đó, bài toán tự động nhận diện bệnh trên lá cây từ ảnh chụp thực địa bằng học máy là một hướng nghiên cứu có giá trị ứng dụng cao.

### 1.1 Phát biểu bài toán

Nhóm xây dựng hệ thống Instance Segmentation trên ảnh lá cây, với mục tiêu:

- **Đầu vào:** Ảnh lá cây chụp ngoài thực địa (có thể chứa nhiều lá, nhiều vùng bệnh).
- **Đầu ra:** Mask pixel-wise xác định vùng bị bệnh kèm theo nhãn loại bệnh tương ứng.
- **Phạm vi:** 8 lớp nhãn được chia đều cho hai đối tượng cây trồng chính:
  - Lúa: Healthy (Khỏe mạnh), BrownSpot (Đốm nâu), Hispa (Sâu gai), LeafBlast (Bệnh đạo ôn).
  - Cà phê: LeafMiner (Bệnh sâu vẽ bùa), PowderyMildew (Bệnh phấn trắng), Rust (Bệnh nấm rỉ sắt), AlgalLeafSpot (Bệnh đốm rong).

#### 1.1.1 Định nghĩa hình thức

Một cách toán học, bài toán phân vùng thực thể bệnh trên lá cây được định nghĩa như sau. Cho ảnh đầu vào $I \in \mathbb{R}^{H \times W \times 3}$, trong đó $H$ và $W$ lần lượt là chiều cao và chiều rộng của ảnh. Mục tiêu của mô hình là tìm tập hợp gồm $K$ thực thể bệnh xuất hiện trong ảnh:

$$E = \{e_1, e_2, \ldots, e_K\} \tag{1}$$

Trong đó, mỗi thực thể $e_k$ ($k \in \{1, 2, \ldots, K\}$) được biểu diễn bằng một bộ ba:

$$e_k = (b_k, c_k, m_k) \tag{2}$$

Với:

- $b_k = [x_{min}, y_{min}, x_{max}, y_{max}] \in \mathbb{R}^4$ là tọa độ của hộp bao (bounding box) giới hạn thực thể $e_k$.
- $c_k \in \{1, 2, \ldots, C\}$ là nhãn lớp bệnh tương ứng với thực thể $e_k$ trong tập $C$ lớp nhãn mục tiêu ($C = 4$ cho từng miền dữ liệu riêng biệt).
- $m_k \in \{0, 1\}^{H \times W}$ là mặt nạ nhị phân (binary mask) xác định vùng bị tổn thương ở cấp độ điểm ảnh (pixel-level) của thực thể $e_k$. Một pixel ở vị trí $(i, j)$ thuộc vết bệnh thứ $k$ nếu $m_k(i, j) = 1$, và bằng $0$ nếu ngược lại.

### 1.2 Lý do chọn Instance Segmentation

Khác với phân loại ảnh chỉ trả về nhãn chung cho cả ảnh, Instance Segmentation:

1. Xác định chính xác vùng bị bệnh trên lá → hỗ trợ nông dân quan sát trực quan.
2. Xử lý được ảnh có nhiều lá chồng chéo hoặc nhiều loại bệnh đồng thời.
3. Phù hợp với điều kiện ảnh thực địa đa dạng về góc chụp, ánh sáng và nền.

---

## 2 Tổng quan dữ liệu đầu vào

### 2.1 Nguồn và quy mô dữ liệu

Bộ dữ liệu được xây dựng từ nhiều nguồn công khai kết hợp công cụ thu thập bán tự động (Human-in-the-loop Labeling Tool). Sau khi loại bỏ ảnh lỗi, trùng lặp và hợp nhất nhãn, tập dữ liệu cuối gồm 7.149 ảnh sạch thuộc 8 lớp bệnh trên hai loại cây:

**Bảng 1: Thống kê bộ dữ liệu sau tiền xử lý**

| Loại cây | Nhãn bệnh | Số ảnh (gốc) | Số ảnh (sạch) |
|---|---|---|---|
| Lúa | Healthy (Khỏe mạnh) | – | – |
| Lúa | BrownSpot (Đốm nâu) | – | – |
| Lúa | Hispa (Sâu gai) | – | – |
| Lúa | LeafBlast (Bệnh đạo ôn) | – | – |
| **Tổng Lúa** | | **3.421** | **3.351** |
| Cà phê | LeafMiner (Bệnh sâu vẽ bùa) | – | – |
| Cà phê | PowderyMildew (Bệnh phấn trắng) | – | – |
| Cà phê | Rust (Bệnh nấm rỉ sắt) | – | – |
| Cà phê | AlgalLeafSpot (Bệnh đốm rong) | – | – |
| **Tổng Cà phê** | | **3.879** | **3.798** |
| **Tổng cộng** | | **7.300** | **7.149** |

### 2.2 Phân chia dữ liệu và thiết lập chung

Dữ liệu thô (raw data) được chia thành ba tập Train / Validation / Test theo tỷ lệ 70/15/15. Phân chia được thực hiện theo chiến lược stratified split để duy trì phân phối lớp đồng đều giữa các tập.

**Bảng 2: Tỷ lệ phân chia tập dữ liệu**

| Tập | Tỷ lệ | Số ảnh |
|---|---|---|
| Train | 70% | 5.004 |
| Validation | 15% | 1.072 |
| Test | 15% | 1.073 |

Lý do chọn tỷ lệ 70/15/15: Tập dữ liệu có quy mô trung bình (∼7.000 ảnh); tỷ lệ này đảm bảo tập Train đủ lớn để học đặc trưng phân vùng, trong khi Validation và Test mỗi tập đủ ∼1.000 ảnh để đánh giá tin cậy về mặt thống kê.

### 2.3 Tiền xử lý ảnh

Tất cả 5 mô hình trong thực nghiệm đều được huấn luyện trên cùng một pipeline tiền xử lý và tăng cường dữ liệu thống nhất nhằm đảm bảo tính công bằng khi so sánh. Kích thước ảnh đầu vào được resize phù hợp với yêu cầu của từng kiến trúc mô hình (chi tiết tại Mục 4).

#### 2.3.1 Chuẩn hóa kích thước

Chuẩn hóa kích thước gồm hai bước:

- **Resize:** Ảnh được resize sử dụng letterbox padding (padding giữ tỷ lệ khung hình gốc) để tránh biến dạng hình học. Kích thước cụ thể phụ thuộc vào từng mô hình.
- **Normalize:** Chuẩn hóa giá trị pixel về [0, 1] rồi chuẩn hóa z-score theo thống kê tập Train.

#### 2.3.2 Xử lý dữ liệu mất cân bằng

Một số lớp bệnh hiếm (ví dụ: PowderyMildew) có số lượng ảnh thấp hơn đáng kể so với các lớp còn lại. Nhóm áp dụng `WeightedRandomSampler` trong DataLoader để đảm bảo mỗi batch huấn luyện có phân phối lớp cân bằng hơn.

#### 2.3.3 Tăng cường dữ liệu

Pipeline augmentation được áp dụng chỉ trên tập Train với các kỹ thuật:

**Bảng 3: Các kỹ thuật tăng cường dữ liệu được sử dụng**

| Kỹ thuật | Tham số | Mục đích |
|---|---|---|
| RandomResizedCrop | scale=(0.5, 1.0) | Đa dạng hóa góc nhìn, scale |
| RandomHorizontalFlip | p=0.5 | Bất biến với lật ngang |
| RandomVerticalFlip | p=0.3 | Bất biến với lật dọc |
| ColorJitter | brightness, contrast, saturation | Đa dạng ánh sáng |
| Affine transform | rotate, shear, translate | Bất biến hình học |
| MixUp | α = 0.4 | Chống overfitting |
| CutMix | α = 1.0 | Chống overfitting |
| CutOut | n_holes=1, length=64 | Tăng cường độ bền |

**Lưu ý:** MixUp và CutMix được áp dụng ở cấp batch (trong vòng lặp huấn luyện), không phải trong DataLoader pipeline, và không áp dụng lên mask segmentation để đảm bảo tính hợp lệ của nhãn pixel.

---

## 3 Lựa chọn mô hình và kiến trúc

Nhóm triển khai và so sánh 5 mô hình segmentation thuộc hai nhóm kiến trúc: CNN-based và Vision Transformer-based (ViT-based). Mỗi mô hình được huấn luyện độc lập trên 2 tập riêng biệt (Rice và Coffee) trên Kaggle Notebook (GPU T4) với cùng một thiết lập huấn luyện chung (chi tiết tại Mục 4).

### 3.1 Tổng quan các mô hình

**Bảng 4: Tổng quan 5 mô hình segmentation được lựa chọn**

| Mô hình | Loại | Đặc điểm nổi bật |
|---|---|---|
| Mask R-CNN | CNN-based | Baseline hai nhánh (detection + segmentation) |
| YOLO26m-seg | CNN-based | Real-time, kiến trúc một nhánh |
| RF-DETR | ViT-based | End-to-end detection transformer (SOTA) |
| MobileSAM | ViT-based | SAM rút gọn, segment anything |
| Mask2Former | ViT-based | Universal segmentation SOTA |

### 3.2 Mô hình 1: Mask R-CNN

#### 3.2.1 Lý do lựa chọn

Mask R-CNN [2] là mô hình instance segmentation CNN nền tảng, được sử dụng làm baseline để so sánh với các mô hình ViT-based. Kiến trúc hai nhánh tách biệt giúp dễ debug và hiểu rõ từng thành phần.

#### 3.2.2 Kiến trúc chi tiết

**1. Sơ đồ kiến trúc:** Kiến trúc chi tiết của mô hình Mask R-CNN được mô tả qua sơ đồ khối dưới đây:

```
Ảnh đầu vào          ResNet-50        Feature Pyramid       Region Proposal
(256 × 256 × 3)  →   Backbone     →   Network (FPN)     →   Network (RPN)
                      (C2 - C5)        (P2 - P6)
                                                               ↓
                                                           RoI Align
                                                               ↓
                                             Fast R-CNN Head          Mask Head
                                           (Phân lớp & BBox)        (FCN Branch)
```

*Hình 1: Sơ đồ kiến trúc mô hình Mask R-CNN với backbone ResNet-50 FPN*

**2. Số lượng tham số:** Mô hình sử dụng cài đặt mặc định từ thư viện torchvision với tổng cộng khoảng 41,8 triệu tham số. Chi tiết:

- Backbone (ResNet-50) & FPN Neck: ≈ 26,8 triệu tham số.
- RPN Head: ≈ 0,6 triệu tham số.
- RoI Heads: ≈ 14,4 triệu tham số (gồm Fast R-CNN Head ≈ 11,8M và Mask Head ≈ 2,6M).

**3. Hàm kích hoạt:**

- Backbone & FPN: ReLU sau mỗi lớp tích chập.
- RPN Head: ReLU sau lớp tích chập trượt; Sigmoid ở nhánh objectness.
- Fast R-CNN Head: ReLU sau các lớp FC; Softmax ở nhánh phân loại.
- Mask Head: ReLU sau tích chập; Sigmoid ở lớp cuối cho mask nhị phân.

#### 3.2.3 Hàm mất mát

Mask R-CNN tối ưu hàm mất mát đa nhiệm (multi-task loss):

$$\mathcal{L} = \mathcal{L}_{rpn\_class} + \mathcal{L}_{rpn\_box} + \mathcal{L}_{fastrcnn\_class} + \mathcal{L}_{fastrcnn\_box} + \mathcal{L}_{mask} \tag{3}$$

Trong đó:

- $\mathcal{L}_{rpn\_class}$: Binary Cross-Entropy Loss cho phân loại vật thể/nền của RPN.
- $\mathcal{L}_{rpn\_box}$: Smooth L1 Loss cho hồi quy tọa độ RPN.
- $\mathcal{L}_{fastrcnn\_class}$: Cross-Entropy Loss cho phân loại lớp bệnh (4 lớp + nền).
- $\mathcal{L}_{fastrcnn\_box}$: Smooth L1 Loss cho hồi quy bounding box.
- $\mathcal{L}_{mask}$: Binary Cross-Entropy Loss pixel-wise trên mask 28×28, chỉ tính cho lớp ground-truth.

### 3.3 Mô hình 2: YOLO26m-seg

#### 3.3.1 Lý do lựa chọn

YOLO26-seg là phiên bản segmentation của họ YOLO [3], thuộc nhóm mô hình CNN one-stage có tốc độ suy luận cao. Nhóm chọn biến thể medium (YOLO26m-seg) để cân bằng giữa dung lượng mô hình và độ chính xác, đặc biệt quan trọng khi triển khai trên web với yêu cầu latency thấp.

#### 3.3.2 Kiến trúc chi tiết

**1. Sơ đồ kiến trúc**

YOLO26m-seg nhận ảnh đầu vào đã được resize/letterbox về 640 × 640, trích xuất đặc trưng bằng backbone CNN, hợp nhất đặc trưng đa tỉ lệ qua neck kiểu FPN/PAN, sau đó dùng segmentation head để dự đoán đồng thời hộp bao, lớp bệnh và mask theo từng instance.

```
Input              Backbone           Neck            Segment head         Output
Ảnh 640×640    →   CNN/C2f blocks →   FPN/PAN     →   Box + class      →   Bounding boxes
letterbox +        trích xuất         hợp nhất        + mask coeff.        instance masks
chuẩn hóa          đặc trưng          đặc trưng        prototype masks
                   đa tỷ lệ
```

*Hình 2: Sơ đồ khối kiến trúc YOLO26m-seg sử dụng trong thực nghiệm*

**2. Số lượng tham số**

Biến thể yolo26m-seg có tổng cộng khoảng 22,4 triệu tham số. Việc lựa chọn cấu hình medium nhằm cân bằng giữa khả năng biểu diễn đặc trưng và tốc độ suy luận khi triển khai thực tế.

**3. Hàm kích hoạt**

Các khối tích chập trong backbone và neck dùng activation SiLU/Swish để giữ gradient ổn định. Ở đầu ra, các nhánh dự đoán sử dụng các phép biến đổi phù hợp: xác suất lớp và hệ số mask được ràng buộc về miền xác suất, còn tọa độ hộp và phân phối DFL được giải mã theo cơ chế YOLO.

#### 3.3.3 Hàm mất mát

YOLO26m-seg tối ưu đồng thời nhiều thành phần mất mát:

$$\mathcal{L} = \lambda_{box}\mathcal{L}_{box} + \lambda_{cls}\mathcal{L}_{cls} + \lambda_{dfl}\mathcal{L}_{dfl} + \lambda_{mask}\mathcal{L}_{mask}$$

Trong đó $\mathcal{L}_{box}$ tối ưu vị trí hộp bao, $\mathcal{L}_{cls}$ tối ưu nhãn bệnh, $\mathcal{L}_{dfl}$ cải thiện độ chính xác biên hộp thông qua phân phối tọa độ, và $\mathcal{L}_{mask}$ tối ưu vùng phân đoạn của instance.

### 3.4 Mô hình 3: RF-DETR

#### 3.4.1 Lý do lựa chọn

RF-DETR là mô hình detection transformer của Roboflow, được thiết kế theo hướng end-to-end cho bài toán phát hiện đối tượng và segmentation. Khác với các mô hình CNN, RF-DETR sử dụng cơ chế truy vấn của Transformer để dự đoán trực tiếp tập đối tượng/mask đầu ra, giảm phụ thuộc vào NMS.

Nhóm sử dụng biến thể RFDETRSegNano và huấn luyện hai mô hình riêng biệt: một cho tập Coffee và một cho tập Rice.

#### 3.4.2 Kiến trúc chi tiết

```
Ảnh đầu vào     Backbone thị giác     Transformer              Prediction Heads       Đầu ra
(640 × 640)  →  Pretrained         →  Encoder/Decoder  →  →   Class, Box,       →    Nhãn lớp
                trích xuất            (Attention            Object Queries         Bounding box
                đặc trưng             mechanism)            Học tham số            Segment mask
```

*Hình 3: Sơ đồ luồng kiến trúc RF-DETR segmentation*

Ảnh được đưa vào backbone để trích xuất đặc trưng thị giác. Các đặc trưng sau đó đi qua các khối Transformer nhằm mô hình hóa quan hệ không gian giữa vùng lá, vùng bệnh và nền ảnh. Prediction head sinh ra ba nhóm đầu ra: nhãn lớp, bounding box và mask. Detection/mask head được khởi tạo lại theo số lớp của từng domain (4 lớp cho mỗi loại cây).

**Hàm kích hoạt.** Backbone dùng activation mặc định của pretrained checkpoint. Transformer feed-forward network dùng GELU/ReLU. Attention dùng Softmax trên attention weights. Classification head sinh class logit, box head dự đoán tọa độ chuẩn hóa, mask head sinh mask probability.

#### 3.4.3 Hàm mất mát

RF-DETR thuộc họ DETR nên quá trình học dựa trên matching giữa prediction queries và ground truth (bipartite matching), kết hợp các thành phần loss:

- Classification loss để học nhãn bệnh của từng prediction.
- Box regression loss để học vị trí vùng bệnh.
- Mask/segmentation loss để học vùng mask bệnh.
- Matching loss theo tinh thần DETR để gán prediction với ground truth theo cách end-to-end.

### 3.5 Mô hình 4: MobileSAM

#### 3.5.1 Lý do lựa chọn

MobileSAM [7] là phiên bản rút gọn của SAM (Segment Anything Model), thay thế ViT-H encoder bằng TinyViT — nhỏ hơn 60× và nhanh hơn 40×, phù hợp deploy. Nhóm fine-tune để áp dụng vào domain bệnh lá cây.

#### 3.5.2 Kiến trúc chi tiết

**1. Sơ đồ kiến trúc:**

```
Input Image          TinyViT                        Mask Decoder       Binary Mask
(1024 × 1024)  →     Image Encoder  →  →  →  →  →  →  →  →  →  →  →  Output
                           ↓
                     Image Embedding
                           ↓
               Prompt Encoder (Bbox/Points)
                           ↓
               Sparse/Dense Embeddings
```

*Hình 4: Sơ đồ luồng kiến trúc MobileSAM áp dụng trong bài toán phân vùng.*

**2. Số lượng tham số:**

Tổng số lượng tham số đạt xấp xỉ 9,66M:

- TinyViT-5M Image Encoder: ≈ 5,79M tham số.
- Prompt Encoder: ≈ 6,2K tham số.
- Mask Decoder: ≈ 3,87M tham số.

**3. Hàm kích hoạt:**

- GELU: Sử dụng trong các khối Transformer của TinyViT và Mask Decoder.
- Sigmoid: Áp dụng tại đầu ra của Mask Decoder để chuyển logits thành xác suất pixel.
- LayerNorm: Sử dụng xuyên suốt các tầng ẩn để ổn định phân phối.

#### 3.5.3 Hàm mất mát

Hàm mất mát tổng hợp của MobileSAM:

$$\mathcal{L}_{total} = 20 \times \mathcal{L}_{Focal} + \mathcal{L}_{Dice} + \mathcal{L}_{MSE} \tag{4}$$

Trong đó:

- **Sigmoid Focal Loss ($\mathcal{L}_{Focal}$):** Giải quyết mất cân bằng pixel giữa vùng bệnh nhỏ và nền lá lành. Hệ số nhân 20 giúp tập trung vào pixel biên khó phân loại.
- **Dice Loss ($\mathcal{L}_{Dice}$):** Tối ưu trực tiếp độ trùng khớp vùng phân vùng (IoU).
- **MSE Loss ($\mathcal{L}_{MSE}$):** Đo lỗi giữa hệ số IoU dự đoán và IoU thực tế, giúp tinh chỉnh độ tin cậy nội bộ.

### 3.6 Mô hình 5: Mask2Former

#### 3.6.1 Lý do lựa chọn

Mask2Former [1] thống nhất ba bài toán segmentation (instance, semantic, panoptic) trong một kiến trúc duy nhất dựa trên cơ chế mask classification. Mô hình đạt kết quả SOTA trên COCO và là đại diện Transformer-based đối lập với baseline CNN (Mask R-CNN).

#### 3.6.2 Kiến trúc chi tiết

Mask2Former gồm ba thành phần: backbone trích đặc trưng đa tỷ lệ, pixel decoder nâng độ phân giải đặc trưng, và Transformer decoder sinh dự đoán theo từng query. Điểm cốt lõi là masked attention: mỗi query chỉ attend vào vùng foreground do chính nó dự đoán ở lớp trước.

```
Ảnh đầu vào     Backbone      Pixel Decoder      Transformer Decoder      Lớp bệnh
H × W × 3  →    Swin-T     →  MSDeformAttn   →   9 lớp, masked        →   (softmax)
                (đặc trưng                        attention                  Mask nhị phân
                đa tỷ lệ)                         N=100 query               (sigmoid)
                                ↓
                        per-pixel embedding
```

*Hình 5: Sơ đồ kiến trúc Mask2Former với backbone Swin-T.*

**Số lượng tham số.** Nhóm sử dụng backbone Swin-T (tiny) với tổng khoảng 47M tham số: Backbone ≈ 28M, Pixel decoder ≈ 10M, Transformer decoder ≈ 9M.

**Hàm kích hoạt.** Mô hình dùng GELU trong MLP của Swin backbone và Transformer decoder, ReLU trong pixel decoder, kèm LayerNorm xuyên suốt. Đầu ra: nhánh phân loại dùng softmax, nhánh mask dùng sigmoid.

#### 3.6.3 Hàm mất mát

Mask2Former tối ưu hàm mất mát mask classification, ghép cặp dự đoán với ground-truth bằng bipartite matching (thuật toán Hungarian):

$$\mathcal{L} = \lambda_{cls}\mathcal{L}_{cls} + \lambda_{ce}\mathcal{L}_{ce} + \lambda_{dice}\mathcal{L}_{dice}$$

trong đó $\mathcal{L}_{cls}$ là cross-entropy cho nhãn lớp, $\mathcal{L}_{ce}$ (binary cross-entropy pixel) và $\mathcal{L}_{dice}$ giám sát chất lượng mask. Trọng số mặc định: $\lambda_{cls}=2$, $\lambda_{ce}=5$, $\lambda_{dice}=5$. BCE ổn định gradient ở mức pixel, trong khi Dice trực tiếp tối ưu độ chồng lấp và ít nhạy với mất cân bằng foreground/background.

---

## 4 Cấu hình huấn luyện

Để đảm bảo so sánh công bằng giữa 5 mô hình, nhóm thiết lập một cấu hình huấn luyện chung thống nhất. Tất cả mô hình đều được huấn luyện trên cùng một tập dữ liệu đã chia (Mục 2), cùng pipeline tiền xử lý và augmentation, với các siêu tham số chung sau:

### 4.1 Thiết lập chung

Bảng 5 thể hiện thiết lập huấn luyện chung cho tất cả 5 mô hình

**Bảng 5: Thiết lập huấn luyện chung cho tất cả 5 mô hình**

| Tham số | Giá trị |
|---|---|
| GPU | NVIDIA Tesla T4 (Kaggle Notebook) |
| Số epoch tối đa | 10 |
| Effective batch size | 8 (một số mô hình dùng gradient accumulation) |
| Thuật toán tối ưu | AdamW (có weight decay) |
| Early stopping patience | 5 epoch |
| Seed | 3407 |
| Phân chia dữ liệu | 70/15/15 (Train/Val/Test), stratified split |
| Tiền xử lý | Pipeline chung (Mục 2) |
| Augmentation | Pipeline chung (Bảng 3) |

Mỗi mô hình có learning rate và kích thước ảnh đầu vào riêng, được chọn phù hợp với yêu cầu kiến trúc của từng mô hình. Chi tiết được trình bày trong Bảng 6.

### 4.2 Tham số riêng theo mô hình

**Bảng 6: Tham số riêng của từng mô hình**

| Mô hình | Learning rate | Image size | Ghi chú |
|---|---|---|---|
| Mask R-CNN | $1 \times 10^{-4}$ | 256 × 256 | Batch size 2, grad accum 4 |
| YOLO26m-seg | $8 \times 10^{-4}$ | 640 × 640 | Batch size 8 |
| RF-DETR | $1 \times 10^{-4}$ | Mặc định thư viện | Batch size 2, grad accum 4 |
| MobileSAM | $1 \times 10^{-5}$ | 1024 × 1024 | Batch size 2, grad accum 4; freeze encoder |
| Mask2Former | $5 \times 10^{-5}$ | 384 | Batch size 4, grad accum 2 |

**Lưu ý:**

- Các mô hình có batch size nhỏ hơn 8 sẽ sử dụng gradient accumulation để đạt effective batch size = 8, đảm bảo sự công bằng trong quá trình tối ưu. Việc sử dụng gradient accumulation sẽ tránh bị lỗi GPU Out of Memory.
- MobileSAM đóng băng hoàn toàn Image Encoder (TinyViT) và Prompt Encoder, chỉ finetune Mask Decoder (≈ 3,87M tham số) để tận dụng khả năng trích xuất đặc trưng tổng quát đã được tiền huấn luyện.
- Tất cả mô hình đều sử dụng checkpoint tốt nhất trên tập Validation (theo mAP@50:95) để đánh giá trên tập Test.

---

## 5 Kết quả thực nghiệm

Phần này trình bày kết quả huấn luyện và đánh giá của 5 mô hình trên cả hai tập dữ liệu Lúa và Cà phê. Tất cả mô hình được huấn luyện với cùng thiết lập chung (Mục 4) nhằm đảm bảo so sánh công bằng.

### 5.1 Biểu đồ quá trình học

Hình 6 và Hình 7 trình bày đường cong học (training loss và validation loss) của 5 mô hình qua 10 epoch trên từng tập dữ liệu.

*Hình 6: Learning curves của 5 mô hình trên tập Lúa. Đường liền: validation loss; đường đứt: training loss.*

*Hình 7: Learning curves của 5 mô hình trên tập Cà phê. Đường liền: validation loss; đường đứt: training loss.*

**Nhận xét:**

- RF-DETR và YOLO26m-seg hội tụ nhanh nhất trên cả hai tập dữ liệu, đạt validation loss thấp nhất trong số 5 mô hình. Hai mô hình này có khoảng cách train–val loss nhỏ, cho thấy khả năng tổng quát hóa tốt và không xảy ra overfitting nghiêm trọng trong 10 epoch.
- Mask2Former hội tụ ổn định, validation loss nằm ở mức trung bình; khoảng cách train–val nhỏ cho thấy mô hình không bị overfitting.
- Mask R-CNN có validation loss cao hơn, đặc biệt trên tập Rice, phản ánh hạn chế của kiến trúc hai giai đoạn với kích thước ảnh nhỏ (256 × 256).
- MobileSAM có validation loss cao nhất do chỉ fine-tune Mask Decoder (≈ 3,87M tham số), hạn chế khả năng học đặc trưng mới. Tuy nhiên, khoảng cách train–val rất nhỏ nhờ đóng băng encoder, hoàn toàn tránh được overfitting.
- Trên tập Coffee, tất cả mô hình đều đạt validation loss thấp hơn so với Rice, cho thấy các vết bệnh trên lá cà phê có đặc trưng thị giác rõ ràng và dễ học hơn.

### 5.2 Đánh giá trên tập Test

Bảng 7 tổng hợp kết quả đánh giá của tất cả 5 mô hình trên tập Test (sử dụng checkpoint tốt nhất theo validation mAP@50:95).

**Bảng 7: Kết quả đánh giá 5 mô hình trên tập Test (Rice và Coffee)**

| Mô hình | Dataset | mAP@50 (↑) | mAP@50:95 (↑) | mIoU (↑) | Dice (↑) | Time (ms) (↓) |
|---|---|---|---|---|---|---|
| Mask R-CNN | Rice | 0,721 | 0,653 | 0,742 | 0,782 | 285,4 |
| Mask R-CNN | Coffee | 0,835 | 0,774 | 0,812 | 0,848 | 271,8 |
| YOLO26m-seg | Rice | 0,862 | 0,801 | 0,836 | 0,868 | 12,3 |
| YOLO26m-seg | Coffee | 0,918 | 0,871 | 0,893 | 0,917 | 11,8 |
| RF-DETR | Rice | 0,885 | 0,826 | 0,854 | 0,885 | 68,5 |
| RF-DETR | Coffee | 0,941 | 0,897 | 0,912 | 0,935 | 65,2 |
| MobileSAM | Rice | 0,612 | 0,548 | 0,621 | 0,658 | 1450,2 |
| MobileSAM | Coffee | 0,738 | 0,682 | 0,704 | 0,741 | 1520,6 |
| Mask2Former | Rice | 0,793 | 0,731 | 0,768 | 0,805 | 92,4 |
| Mask2Former | Coffee | 0,876 | 0,828 | 0,851 | 0,882 | 88,7 |

**Nhận xét và phân tích:**

- **RF-DETR đạt hiệu năng cao nhất trên tất cả các metric** ở cả hai tập dữ liệu. Trên Coffee, mAP@50:95 đạt 0,897 và Dice đạt 0,935; trên Rice, mAP@50:95 đạt 0,826 và Dice đạt 0,885. Cơ chế attention toàn cục của Transformer giúp mô hình nắm bắt tốt quan hệ ngữ cảnh giữa vùng bệnh và nền lá.
- **YOLO26m-seg có hiệu năng rất sát RF-DETR**, chỉ thấp hơn khoảng 2–3 đơn vị phần trăm trên các metric chính (mAP@50:95 Rice: 0,801 vs 0,826; Coffee: 0,871 vs 0,897). Tuy nhiên, YOLO26m-seg có **tốc độ suy luận nhanh nhất, gấp ∼5,5× so với RF-DETR** (12,3 ms vs 68,5 ms trên Rice) — đây là lợi thế quyết định khi triển khai ứng dụng thời gian thực.
- **Mask2Former** đạt kết quả ổn định ở mức trung bình–khá, mAP@50:95 đạt 0,731 (Rice) và 0,828 (Coffee), với tốc độ suy luận ∼90 ms.
- **Mask R-CNN** (baseline CNN) có hiệu năng thấp hơn các mô hình Transformer, đặc biệt trên Rice (0,653 mAP@50:95). Kích thước ảnh nhỏ (256 × 256) hạn chế khả năng phát hiện vết bệnh nhỏ. Tốc độ suy luận chậm (∼280 ms) do kiến trúc hai giai đoạn.
- **MobileSAM** có hiệu năng thấp nhất do chỉ fine-tune Mask Decoder. Tuy nhiên, mô hình vẫn đạt mIoU > 0,62 nhờ thừa hưởng khả năng trích xuất đặc trưng tổng quát từ pretrained TinyViT. Tốc độ suy luận rất chậm (> 1400 ms) do kiến trúc nặng của SAM.
- Trên cả hai tập dữ liệu, **Coffee luôn cho kết quả tốt hơn Rice**. Nguyên nhân: vết bệnh trên lá cà phê (gỉ sắt, đốm rong) thường có đặc trưng màu sắc tương phản mạnh và ranh giới rõ ràng hơn so với vết bệnh nhỏ, phân tán trên lá lúa.

### 5.3 Confusion Matrix

Các ma trận nhầm lẫn chuẩn hóa theo dòng được xây dựng dựa trên dự đoán có IoU ≥ 0,5 với ground truth trên tập Test.

*Hình 8: Confusion matrix của Mask R-CNN trên tập Test.*

**Nhận xét (Mask R-CNN):** Trên Rice, nhầm lẫn xảy ra nhiều nhất giữa *Đốm nâu* và *Bệnh đạo ôn* do hai vết bệnh có nhân màu nâu sẫm tương đồng. Lớp *Khỏe mạnh* được phân loại tốt nhất. Trên Coffee, *Bệnh phấn trắng* đạt độ chính xác cao nhờ đặc trưng màu sắc riêng biệt; nhầm lẫn chủ yếu xảy ra giữa *Bệnh nấm rỉ sắt* và *Bệnh đốm rong*.

*Hình 9: Confusion matrix của YOLO26m-seg trên tập Test.*

**Nhận xét (YOLO26m-seg):** Mô hình đạt độ chính xác cao trên hầu hết các lớp. Trên Rice, lớp *Khỏe mạnh* đạt recall > 0,95, các lớp bệnh cũng đạt > 0,83. Nhầm lẫn còn lại chủ yếu giữa *Sâu gai* và *Đốm nâu*. Trên Coffee, *Bệnh phấn trắng* gần như được nhận diện hoàn hảo (> 0,96).

*Hình 10: Confusion matrix của RF-DETR trên tập Test.*

**Nhận xét (RF-DETR):** RF-DETR đạt recall cao nhất trên hầu hết các lớp. Trên Rice, *Khỏe mạnh* đạt > 0,96 và *Bệnh đạo ôn* đạt > 0,87. Trên Coffee, tất cả các lớp đều đạt recall > 0,90, đặc biệt *Bệnh phấn trắng* đạt > 0,97. Mức nhầm lẫn giữa các lớp rất thấp nhờ cơ chế attention toàn cục giúp nắm bắt ngữ cảnh.

*Hình 11: Confusion matrix của MobileSAM trên tập Test.*

**Nhận xét (MobileSAM):** Mức nhầm lẫn cao hơn các mô hình khác, đặc biệt giữa *Đốm nâu*–*Bệnh đạo ôn* trên Rice và *Bệnh nấm rỉ sắt*–*Bệnh đốm rong* trên Coffee. Nguyên nhân: chỉ fine-tune Mask Decoder nên khả năng phân biệt nhãn lớp hạn chế. Tuy nhiên, lớp có đặc trưng rõ (*Khỏe mạnh*, *Bệnh phấn trắng*) vẫn đạt recall khá (> 0,80).

*Hình 12: Confusion matrix của Mask2Former trên tập Test.*

**Nhận xét (Mask2Former):** Hiệu năng phân loại ở mức khá tốt, đặc biệt trên Coffee. Cơ chế masked attention giúp mô hình tập trung vào vùng foreground, giảm nhầm lẫn so với Mask R-CNN. Nhầm lẫn còn lại tập trung ở các cặp lớp có đặc trưng thị giác gần nhau, tương tự các mô hình khác.

### 5.4 Phân tích lỗi và các trường hợp dự đoán sai

Để hiểu rõ hơn về các hạn chế hiện tại của mô hình, nhóm tiến hành phân tích định tính các mẫu dữ liệu dự đoán sai tiêu biểu của mô hình baseline Mask R-CNN trên tập Test (được trực quan hóa trong Hình 13).

*Hình 13: Các ví dụ trực quan về dự đoán sai (ảnh gốc, nhãn thực tế Ground Truth và dự đoán của mô hình Mask R-CNN) trên tập dữ liệu Rice.*

Dựa trên kết quả trực quan ở Hình 13, các lỗi sai của mô hình tập trung vào hai nhóm nguyên nhân chính:

**1. Sự mập mờ về ranh giới đặc trưng thị giác ở mức vi mô (Ambiguous microfeatures):**

- **Mô tả lỗi:** Ở các mẫu lá lúa Image 577, Image 579 và Image 580, Ground Truth dán nhãn cho toàn bộ chiếc lá là lớp Healthy (được biểu thị bằng màu xanh lá). Tuy nhiên, mô hình Mask R-CNN lại dự đoán nhãn BrownSpot (Bệnh đốm nâu) với độ tin cậy rất cao (lần lượt là 0.96, 0.72, 0.87) và tô đỏ toàn bộ chiếc lá.
- **Giả thuyết nguyên nhân:** Trên thực tế, trên các phiến lá Healthy này xuất hiện các vết đốm hoại tử rất nhỏ, các đốm xước cơ học li ti hoặc các đốm vàng do thiếu chất dinh dưỡng nhẹ. Những đốm nhỏ này có đặc trưng hình học (hình chấm tròn nhỏ) và màu sắc (nâu sẫm/vàng nhạt) rất tương đồng với triệu chứng ban đầu của bệnh đốm nâu. Do đó, mô hình baseline dễ bị nhầm lẫn bởi các "nhiễu vi mô" này và phóng đại kết quả phân loại thành bệnh đốm nâu cho toàn bộ chiếc lá. Ranh giới đặc trưng giữa "lá khỏe mạnh có tì vết nhỏ" và "lá bị bệnh đốm nâu giai đoạn chớm nở" là cực kỳ mong manh, khiến mô hình gặp khó khăn lớn trong việc phân biệt.

**2. Lỗi định vị vùng (Localization/Segmentation leakage) do nhiễu nền:**

- **Mô tả lỗi:** Ở mẫu Image 578, ảnh gốc chứa một chiếc lá lúa xanh nằm dọc ở mép trái với phần nền trắng. Nhãn Ground Truth khoanh vùng chính xác chiếc lá này. Tuy nhiên, mô hình dự đoán nhãn BrownSpot (0.84) và LeafBlast (0.58) đồng thời tạo ra một mặt nạ (mask) khổng lồ màu đỏ bao phủ gần như toàn bộ bức ảnh bao gồm cả nền trống.
- **Giả thuyết nguyên nhân:** Đây là một lỗi nghiêm trọng liên quan đến nhánh đề xuất vùng (RPN - Region Proposal Network) và cơ chế RoI Align của Mask R-CNN. Khi độ tương phản của biên vật thể so với nền không đủ mạnh hoặc do sự phân tán đặc trưng từ các bộ lọc tích chập, mô hình đã đề xuất một vùng anchor quá lớn (bao phủ cả nền) và không thể giới hạn mặt nạ bên trong biên chiếc lá. Lỗi này phản ánh điểm hạn chế của kiến trúc CNN hai giai đoạn khi xử lý các vật thể dài, mảnh trên nền sáng, dễ bị ảnh hưởng bởi sự lan truyền lỗi (error propagation) từ giai đoạn đề xuất vùng sang giai đoạn phân đoạn pixel.

---

## 6 Thảo luận và lựa chọn mô hình

### 6.1 So sánh tổng hợp các mô hình

Dựa trên kết quả thực nghiệm tại Bảng 7, nhóm tổng hợp so sánh đa tiêu chí giữa 5 mô hình trong Bảng 8.

**Bảng 8: Bảng so sánh đa tiêu chí giữa 5 mô hình phân vùng thực thể**

| Tiêu chí | Mask R-CNN | YOLO26m-seg | RF-DETR | MobileSAM | Mask2Former |
|---|---|---|---|---|---|
| **Tập dữ liệu Lúa (Rice)** | | | | | |
| mAP@50:95 | 0,653 | 0,801 | 0,826 | 0,548 | 0,731 |
| mIoU | 0,742 | 0,836 | 0,854 | 0,621 | 0,768 |
| Time (ms) | 285,4 | 12,3 | 68,5 | 1450,2 | 92,4 |
| **Tập dữ liệu Cà phê (Coffee)** | | | | | |
| mAP@50:95 | 0,774 | 0,871 | 0,897 | 0,682 | 0,828 |
| mIoU | 0,812 | 0,893 | 0,912 | 0,704 | 0,851 |
| Time (ms) | 271,8 | 11,8 | 65,2 | 1520,6 | 88,7 |

**Phân tích:**

- **RF-DETR** đạt hiệu năng cao nhất trên tất cả metric segmentation (mAP@50, mAP@50:95, mIoU, Dice) ở cả hai tập dữ liệu. Cơ chế Transformer cho phép mô hình học được quan hệ ngữ cảnh toàn cục giữa các vùng bệnh và nền lá.
- **YOLO26m-seg** có hiệu năng rất sát RF-DETR — chỉ chênh khoảng 2–3 đơn vị phần trăm (mAP@50:95 Rice: 0,801 vs 0,826; Coffee: 0,871 vs 0,897). Tuy nhiên, YOLO26m-seg có tốc độ suy luận nhanh nhất, gấp ∼5,5× so với RF-DETR (12,3 ms vs 68,5 ms).
- Các mô hình còn lại (Mask2Former, Mask R-CNN, MobileSAM) có hiệu năng thấp hơn đáng kể hoặc tốc độ suy luận quá chậm cho triển khai thời gian thực.

### 6.2 Lựa chọn mô hình triển khai

Dựa trên phân tích trên, nhóm lựa chọn **YOLO26m-seg** làm mô hình triển khai cuối cùng cho cả hai tập dữ liệu Lúa và Cà phê. Lý do:

1. **Độ chính xác tốt:** mAP@50:95 đạt 0,801 (Rice) và 0,871 (Coffee), chỉ thấp hơn RF-DETR khoảng 2–3%.
2. **Tốc độ suy luận nhanh nhất:** ∼12 ms/ảnh, hoàn toàn đáp ứng yêu cầu suy luận thời gian thực trên web (< 200 ms).
3. **Kích thước nhỏ gọn:** Phù hợp triển khai trên máy chủ web có tài nguyên hạn chế.
4. **Tiết kiệm tài nguyên:** Vì tất cả mô hình đều là deep learning và tốn nhiều tài nguyên tính toán, việc chỉ tinh chỉnh và triển khai một mô hình duy nhất giúp tiết kiệm thời gian và chi phí đáng kể.

### 6.3 Hyperparameter Tuning cho YOLO26m-seg

Sau khi chọn YOLO26m-seg làm mô hình triển khai, nhóm tiến hành thực hiện hyperparameter tuning nhằm tối ưu hóa hiệu năng mô hình trước khi triển khai thực tế.

#### 6.3.1 Phương pháp: Ray Tune với ASHAScheduler

Nhóm sử dụng thư viện Ray Tune kết hợp với thuật toán ASHA (Asynchronous Successive Halving Algorithm) để tìm kiếm siêu tham số tối ưu. ASHA là một thuật toán early-stopping thông minh cho hyperparameter search, hoạt động bằng cách:

- Khởi tạo nhiều thử nghiệm (trials) với các cấu hình siêu tham số khác nhau.
- Dừng sớm (early stop) các thử nghiệm có hiệu năng kém sau mỗi vòng đánh giá.
- Phân bổ tài nguyên nhiều hơn cho các thử nghiệm có triển vọng tốt.

Phương pháp này đặc biệt hiệu quả cho các mô hình deep learning vì tiết kiệm đáng kể thời gian GPU so với Grid Search hay Random Search truyền thống.

#### 6.3.2 Thiết lập thực nghiệm

Quá trình tinh chỉnh được thực hiện trên Kaggle Notebook với 2 GPU T4, cho phép chạy đồng thời nhiều trial. Không gian tìm kiếm siêu tham số (search space) bao gồm:

**Bảng 9: Không gian tìm kiếm siêu tham số cho YOLO26m-seg**

| Siêu tham số | Kiểu phân phối | Khoảng giá trị |
|---|---|---|
| Learning rate | Log-uniform | $[1 \times 10^{-5}, 1 \times 10^{-2}]$ |
| Momentum | Uniform | [0,85; 0,95] |
| Weight decay | Log-uniform | $[1 \times 10^{-5}, 1 \times 10^{-3}]$ |
| Warmup epochs | Choice | {1, 2, 3} |
| Box loss gain | Uniform | [5,0; 10,0] |
| Cls loss gain | Uniform | [0,3; 0,8] |

#### 6.3.3 Kết quả tinh chỉnh

Sau khi chạy ASHA với 20 trial, bộ siêu tham số tối ưu được xác định và mô hình YOLO26m-seg được huấn luyện lại với cấu hình tốt nhất. Kết quả so sánh trước và sau khi tinh chỉnh được trình bày trong Bảng 10.

**Bảng 10: Kết quả YOLO26m-seg trước và sau khi tinh chỉnh siêu tham số**

| Cấu hình | Dataset | mAP@50 | mAP@50:95 | mIoU | Dice |
|---|---|---|---|---|---|
| Trước tuning | Rice | 0,862 | 0,801 | 0,836 | 0,868 |
| Trước tuning | Coffee | 0,918 | 0,871 | 0,893 | 0,917 |
| Sau tuning (ASHA) | Rice | 0,891 | 0,834 | 0,862 | 0,893 |
| Sau tuning (ASHA) | Coffee | 0,948 | 0,903 | 0,921 | 0,942 |

**Nhận xét:**

- Sau khi tinh chỉnh, YOLO26m-seg cải thiện đáng kể trên cả hai tập dữ liệu: mAP@50:95 tăng +3,3% trên Rice và +3,2% trên Coffee.
- Kết quả sau tuning của YOLO26m-seg (0,834 và 0,903) vượt qua cả RF-DETR (0,826 và 0,897), xác nhận tính đúng đắn của quyết định chọn YOLO26m-seg để triển khai.
- Tốc độ suy luận không thay đổi sau tuning (∼12 ms/ảnh) vì kiến trúc mô hình không bị thay đổi.
- Việc sử dụng Ray Tune + ASHA trên 2 GPU T4 giúp hoàn thành quá trình tìm kiếm trong thời gian ngắn, minh chứng cho hiệu quả của phương pháp tinh chỉnh tự động so với thử nghiệm thủ công.

---

## 7 Kết luận

Đồ án đã nghiên cứu và xây dựng thành công hệ thống phân vùng thực thể chẩn đoán bệnh trên lá lúa và lá cà phê dựa trên các mô hình học sâu hiện đại. Qua toàn bộ quá trình thực hiện từ tiền xử lý dữ liệu đến huấn luyện và đánh giá mô hình, nhóm nghiên cứu rút ra các kết luận sau:

**1. Tóm tắt quy trình:** Nhóm đã xây dựng và làm sạch bộ dữ liệu thực địa gồm 7.149 ảnh chất lượng cao phân bố trên 8 lớp nhãn bệnh của cây lúa và cà phê. Năm mô hình đại diện cho hai trường phái kiến trúc chính (CNN-based và Vision Transformer-based) bao gồm Mask R-CNN, YOLO26m-seg, RF-DETR, MobileSAM và Mask2Former đã được huấn luyện trên cùng một thiết lập thống nhất (10 epoch, effective batch size 8, AdamW, seed 3407, GPU T4) và đánh giá toàn diện bằng các chỉ số kiểm thử nghiêm ngặt (mAP@50, mAP@50:95, mIoU, Dice Score, tốc độ suy luận).

**2. Kết quả nổi bật:**

- RF-DETR đạt hiệu năng cao nhất trên tất cả metric segmentation (mAP@50:95 đạt 0,826 trên Rice và 0,897 trên Coffee).
- YOLO26m-seg có hiệu năng rất sát RF-DETR (chỉ chênh 2–3%) nhưng có tốc độ suy luận nhanh nhất (∼12 ms/ảnh, gấp ∼5,5× RF-DETR).
- Nhóm lựa chọn YOLO26m-seg để triển khai cho cả hai tập dữ liệu nhờ sự cân bằng tối ưu giữa độ chính xác và tốc độ.
- Sau khi tinh chỉnh siêu tham số bằng Ray Tune + ASHAScheduler (2 GPU T4), YOLO26m-seg cải thiện thêm ∼3% và vượt qua cả RF-DETR: mAP@50:95 đạt 0,834 (Rice) và 0,903 (Coffee).

**3. Hạn chế của hệ thống:**

- Mô hình vẫn gặp khó khăn khi phát hiện các vết bệnh ở giai đoạn đầu có kích thước siêu nhỏ (chỉ vài pixel) do sự tiêu biến thông tin không gian qua các tầng trích xuất đặc trưng sâu.
- Sự tương đồng về mặt thị giác giữa một số loại bệnh (như Đốm nâu và Bệnh đạo ôn trên lúa, Bệnh nấm rỉ sắt và Bệnh đốm rong trên cà phê) làm gia tăng tỷ lệ phân loại nhầm lẫn nhãn lớp.

**4. Hướng phát triển tiếp theo:**

- Tích hợp mô hình YOLO26m-seg thành một pipeline thống nhất, tự động nhận diện loại cây trồng trước khi chẩn đoán bệnh.
- Thu thập thêm mẫu dữ liệu của các lớp thiểu số để nâng cao độ bền vững và khả năng chẩn đoán toàn diện của hệ thống ngoài thực địa.
- Nghiên cứu tối ưu hóa mô hình qua lượng tử hóa và xuất sang định dạng phù hợp để triển khai trên thiết bị di động của nông dân.

---

## Tài liệu tham khảo

[1] Bowen Cheng, Ishan Misra, Alexander G. Schwing, Alexander Kirillov, and Rohit Girdhar. Masked-attention mask transformer for universal image segmentation. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, pages 1290–1299, 2022.

[2] Kaiming He, Georgia Gkioxari, Piotr Dollar, and Ross Girshick. Mask R-CNN. In *Proceedings of the IEEE International Conference on Computer Vision (ICCV)*, pages 2961–2969, 2017.

[3] Glenn Jocher, Ayush Chaurasia, and Jing Qiu. Ultralytics YOLO. 2023. Version 8.0.0.

[4] Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C Berg, Wan-Yen Lo, et al. Segment anything. In *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, pages 4015–4024, 2023.

[5] Richard Liaw, Eric Liang, Robert Nishihara, Philipp Moritz, Joseph E. Gonzalez, and Ion Stoica. Tune: A research platform for distributed model selection and training. In *ICML AutoML Workshop*, 2018.

[6] Roboflow. RF-DETR: A real-time object detection transformer, 2024. Accessed: 2025.

[7] Junlong Zhang, Yanpeng Sun, Qian Zhang, and Xiaosong Zhang. MobileSAM: Fast segment anything. *arXiv preprint arXiv:2306.14289*, 2023.
