# ĐẠI HỌC QUỐC GIA TPHCM
## TRƯỜNG ĐẠI HỌC KHOA HỌC TỰ NHIÊN
### KHOA CÔNG NGHỆ THÔNG TIN

---

# BÁO CÁO VỀ DỮ LIỆU

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

Ngày 2 tháng 5 năm 2026

---

## Mục lục

- Danh sách bảng
- Danh sách hình vẽ
- Bảng thuật ngữ
1. Giới thiệu bài toán
2. Thu thập và Chuẩn bị dữ liệu
   - 2.1 Động lực và bối cảnh
   - 2.2 Tổng quan pipeline thu thập dữ liệu
   - 2.3 Xây dựng truy vấn tìm kiếm theo ngữ cảnh tiếng Việt
   - 2.4 Cào dữ liệu ảnh và ngữ cảnh văn bản
   - 2.5 Gán nhãn tự động bằng Gemma 4
   - 2.6 Kiểm duyệt thủ công bằng công cụ gán nhãn tự xây dựng
   - 2.7 Mở rộng sang bài toán segmentation với SAM 3
   - 2.8 Cấu trúc lưu trữ và tính toàn vẹn dữ liệu
   - 2.9 Thảo luận và hạn chế
3. Phân tích khám phá dữ liệu (EDA)
   - 3.1 Thách thức của tập dữ liệu nông nghiệp
   - 3.2 Tổng quan tập dữ liệu
   - 3.3 Phân phối lớp dữ liệu
   - 3.4 Phân tích kích thước và tỉ lệ ảnh
   - 3.5 Phân tích độ sáng và kênh màu RGB
   - 3.6 Trực quan hóa mẫu bệnh
   - 3.7 Phân tích annotation COCO
   - 3.8 Nhận diện cặp bệnh dễ nhầm lẫn
   - 3.9 Chỉ số đánh giá Macro F1-score
   - 3.10 Tóm tắt phát hiện và quyết định kỹ thuật
4. Tiền xử lý dữ liệu
   - 4.1 Xây dựng bảng metadata hợp nhất từ dữ liệu thô
   - 4.2 Làm sạch dữ liệu: invalid, duplicate, blurry
   - 4.3 Chia dữ liệu chống leakage (Stratified Split)
   - 4.4 Chuẩn hóa ảnh và lưu vào data/processed/images
   - 4.5 Tính thống kê chuẩn hóa (mean/std) trên train split
   - 4.6 Thiết lập augmentation cho train/val/test
   - 4.7 Cân bằng lớp cho train loader và lưu cấu hình tiền xử lý
   - 4.8 Kết luận và đầu ra của giai đoạn tiền xử lý
- Tài liệu tham khảo

---

## Danh sách bảng

| Số | Mô tả |
|----|-------|
| 2 | Trích lược bộ truy vấn tiếng Việt theo cây trồng và nhãn bệnh |
| 3 | Thống kê tổng quan theo domain |
| 4 | Phân phối lớp chi tiết của tập dữ liệu |
| 5 | Chỉ số mất cân bằng lớp theo domain |
| 6 | Thống kê hình học ảnh |
| 7 | Thống kê độ sáng và tương phản theo lớp (mẫu 50 ảnh/lớp) |
| 8 | Thống kê annotation quan trọng |
| 9 | Khoảng cách Bhattacharyya theo kênh màu cho các cặp dễ nhầm |
| 10 | Tóm tắt các phát hiện chính từ EDA |
| 11 | Thống kê số ảnh và kích thước trung bình theo lớp trước làm sạch |
| 12 | Tổng hợp kết quả làm sạch dữ liệu |
| 13 | Phân bố số ảnh theo lớp sau khi làm sạch |
| 14 | Phân bố số ảnh theo split, domain và lớp sau khi chia stratified |
| 15 | Tỉ lệ split toàn cục sau chia dữ liệu |
| 16 | Thống kê normalization tính trên train split |
| 17 | Lý do chọn kỹ thuật augmentation và tham số chính |
| 18 | Thống kê class count và sampling weight trong train split |
| 19 | Tóm tắt đầu ra định lượng quan trọng của giai đoạn preprocessing |

---

## Danh sách hình vẽ

| Số | Mô tả |
|----|-------|
| 1 | Sơ đồ pipeline thu thập và gán nhãn dữ liệu theo hướng human-in-the-loop |
| 2 | Phân phối lớp dữ liệu của hai domain (biểu đồ cột và biểu đồ tròn) |
| 3 | Phân tích kích thước ảnh gồm: tương quan Width–Height, phân phối chiều rộng và phân phối aspect ratio |
| 4 | Phân phối độ sáng, giá trị trung bình RGB và độ tương phản theo lớp bệnh |
| 5 | Lưới mẫu ảnh bệnh của hai domain |
| 6 | Lưới mẫu ảnh bệnh của hai domain |
| 7 | Phân tích annotation COCO: số annotation trên mỗi ảnh, tỉ lệ BBox/ảnh và phân phối log(BBox Area + 1) |
| 8 | So sánh histogram RGB trên các cặp bệnh dễ nhầm lẫn |
| 9 | Biểu đồ phân bố blur score theo domain và ngưỡng lọc mờ toàn cục (q=0.02) |

---

## Bảng thuật ngữ

### Thuật ngữ kỹ thuật chung

| Tiếng Anh | Tiếng Việt |
|-----------|------------|
| Annotation | Gán nhãn hoặc chú giải dữ liệu. |
| Aspect ratio | Tỉ lệ khung hình của ảnh. |
| Bounding box | Hộp giới hạn bao quanh đối tượng quan tâm. |
| Checkpoint | Điểm lưu tiến trình để có thể tiếp tục chạy lại từ trạng thái gần nhất. |
| Classification | Bài toán hoặc tác vụ phân loại. |
| Click segmentation | Phân đoạn ảnh dựa trên điểm nhấp làm tín hiệu gợi ý. |
| Context | Phần ngữ cảnh văn bản đi kèm ảnh, ví dụ alt hoặc mô tả. |
| Crawler | Trình thu thập dữ liệu web tự động. |
| Data augmentation | Tăng cường dữ liệu bằng các phép biến đổi ảnh. |
| Dataset | Bộ dữ liệu. |
| Domain shift | Độ lệch miền dữ liệu giữa tập huấn luyện và dữ liệu thực tế. |
| Duplicate image | Ảnh trùng lặp nội dung. |
| Human-in-the-loop | Quy trình có con người tham gia kiểm duyệt hoặc hiệu chỉnh kết quả của AI. |
| Invalid image | Ảnh không hợp lệ hoặc không đúng đối tượng quan tâm. |
| Metadata | Siêu dữ liệu mô tả mẫu ảnh, nhãn, đường dẫn, kích thước hoặc nguồn gốc. |
| Prompt | Câu lệnh hoặc chỉ dẫn đầu vào dành cho mô hình. |
| Promptable concept segmentation | Phân đoạn khái niệm theo prompt văn bản hoặc vùng gợi ý. |
| Pseudo-mask | Mặt nạ giả được mô hình sinh tự động trước khi refine thủ công. |
| Segmentation | Bài toán phân đoạn ảnh ở mức vùng hoặc điểm ảnh. |
| Visual language model (VLM) | Mô hình thị giác – ngôn ngữ, xử lý đồng thời ảnh và văn bản. |
| Weak label | Nhãn tạm hoặc nhãn yếu, chỉ dùng như tín hiệu gợi ý ban đầu. |

### Nhãn bệnh sử dụng trong báo cáo

| Tiếng Anh | Tiếng Việt |
|-----------|------------|
| Healthy | Khỏe mạnh. |
| BrownSpot | Bệnh đốm nâu. |
| Hispa | Sâu gai hại lúa. |
| LeafBlast | Bệnh đạo ôn lá lúa. |
| LeafMiner | Bệnh sâu vẽ bùa trên lá cà phê. |
| PowderyMildew | Bệnh phấn trắng. |
| Rust | Bệnh nấm rỉ sắt. |
| AlgalLeafSpot | Bệnh đốm rong. |
| Invalid | Nhãn dùng cho ảnh bị loại vì không đúng cây trồng hoặc không đủ giá trị sử dụng. |

---

## 1 Giới thiệu bài toán

Sản xuất lúa gạo và cà phê giữ vai trò quan trọng trong nông nghiệp Việt Nam, nhưng năng suất và chất lượng mùa vụ thường bị ảnh hưởng bởi các bệnh xuất hiện trên lá. Trong thực tế, nhiều nông hộ chưa thể tiếp cận kịp thời nguồn tư vấn chuyên môn, dẫn đến việc nhận diện bệnh chậm hoặc xử lý chưa phù hợp. Từ bối cảnh đó, nhóm hướng tới xây dựng một hệ thống học máy hỗ trợ chẩn đoán bệnh trên lá lúa và lá cà phê từ ảnh chụp bằng điện thoại.

Về bản chất, đây là bài toán phân loại ảnh nhiều lớp. Đầu vào của hệ thống là ảnh lá cây trong điều kiện sử dụng thực tế; đầu ra là nhãn tương ứng với trạng thái khỏe mạnh hoặc một số bệnh phổ biến trên lúa và cà phê đã được chuẩn hóa trong quá trình xây dựng dữ liệu. Mục tiêu của hệ thống là cung cấp dự đoán nhanh, nhất quán và đủ tin cậy để hỗ trợ người dùng trong bước tham khảo ban đầu.

Bài toán này có ý nghĩa thực tiễn cao nhưng cũng chứa nhiều thách thức. Ảnh thu thập ngoài thực tế có thể khác nhau đáng kể về ánh sáng, góc chụp, nền ảnh, độ rõ nét và mức độ che khuất; đồng thời, biểu hiện của các bệnh ở giai đoạn sớm có thể khá giống nhau. Vì vậy, nhóm định hướng xây dựng một hệ thống có khả năng nhận diện tốt trên dữ liệu gần với bối cảnh sử dụng thật, thay vì chỉ đạt kết quả tốt trong điều kiện ảnh lý tưởng.

---

## 2 Thu thập và Chuẩn bị dữ liệu

### 2.1 Động lực và bối cảnh

Một trong những thách thức lớn nhất khi xây dựng hệ thống chẩn đoán bệnh trên lá cây nông nghiệp đặc sản của Việt Nam là sự khan hiếm dữ liệu ảnh có gán nhãn theo đúng ngữ cảnh bản địa. Các bộ dữ liệu công khai hiện có (PlantVillage, Rice Leaf Diseases Dataset, RoCoLe,...) tuy đa dạng về nhãn bệnh nhưng thường được chụp trong điều kiện phòng thí nghiệm hoặc tại các vùng địa lý khác, dẫn tới hiện tượng độ lệch miền dữ liệu khi áp dụng trên ảnh do nông dân Việt Nam chụp trực tiếp bằng điện thoại ngoài đồng ruộng. Để giảm thiểu khoảng cách miền này, nhóm chủ trương mở rộng hai bộ dataset có sẵn là **Rice Diseases Image Dataset** và **Detect Disease On Coffee Leaves**, bằng cách thu thập thêm ảnh từ các trang web, blog và tài liệu kỹ thuật nông nghiệp tiếng Việt.

Hai bộ dữ liệu trên đều được thu thập tại Việt Nam. Cụ thể, **Rice Diseases Image Dataset** gồm hơn 3.300 ảnh chụp trên các cánh đồng lúa ở Việt Nam trong giai đoạn từ tháng 4 đến tháng 5 năm 2019, với bốn nhãn Healthy (Khỏe mạnh), BrownSpot (Đốm nâu), Hispa (Sâu gai) và LeafBlast (Đạo ôn). Trong khi đó, **Detect Disease On Coffee Leaves** do nhóm tự thu thập tại một số vườn cà phê ở huyện Lạc Dương và thành phố Đà Lạt, tỉnh Lâm Đồng, bằng camera của điện thoại iPhone 7 Plus. Nhìn chung, dữ liệu tập trung vào hai cây trồng chủ lực là lúa và cà phê; với cà phê, nhóm sử dụng bốn nhãn LeafMiner (Bệnh sâu vẽ bùa), PowderyMildew (Bệnh phấn trắng), Rust (Bệnh nấm rỉ sắt) và AlgalLeafSpot (Bệnh đốm rong).

### 2.2 Tổng quan pipeline thu thập dữ liệu

Nhóm thiết kế một quy trình thu thập dữ liệu bán tự động theo hướng human-in-the-loop, bao gồm sáu giai đoạn kế tiếp nhau (Hình 1 minh họa):

1. Xây dựng truy vấn tìm kiếm bằng tiếng Việt cho từng nhãn bệnh.
2. Khám phá URL thông qua các công cụ tìm kiếm (DuckDuckGo hoặc Serper.dev).
3. Cào dữ liệu ảnh và văn bản ngữ cảnh bằng thư viện Crawl4AI.
4. Lưu trữ ảnh thô và văn bản đi kèm theo cấu trúc thư mục chuẩn hóa.
5. Gán nhãn tự động bằng Gemma 4. Mô hình sẽ quyết định nhãn cho ảnh dựa vào văn bản ngữ cảnh.
6. Kiểm duyệt thủ công thông qua công cụ gán nhãn được nhóm tự phát triển bằng Streamlit.

Toàn bộ pipeline được hiện thực trong thư mục `crawl/` của mã nguồn dự án, gồm các môđun `search.py`, `crawl_rice_data.py`, `crawl_coffee_data.py`, `utils.py` và `labeler.py`. Pipeline được viết theo mô hình bất đồng bộ để tăng thông lượng khi truy cập web song song, đồng thời có cơ chế checkpoint (qua các tệp `processed_urls.txt` và `pending_images.jsonl`) để đảm bảo khả năng khôi phục khi bị gián đoạn.

**Hình 1:** Sơ đồ pipeline thu thập và gán nhãn dữ liệu theo hướng human-in-the-loop.

> **Pipeline các bước:**
> 1. Xây dựng truy vấn → Từ khóa tiếng Việt cho từng nhãn bệnh
> 2. Khám phá URL → DuckDuckGo / Serper.dev và loại URL trùng
> 3. Cào dữ liệu → Ảnh gốc và văn bản ngữ cảnh bằng Crawl4AI
> 4. Lưu trữ dữ liệu thô → Lưu ảnh và context theo thư mục chuẩn hóa
> 5. AI gán nhãn tự động → Gemma 4 dự đoán nhãn hoặc Invalid
> 6. Kiểm duyệt thủ công → Công cụ Streamlit xác nhận hoặc sửa nhãn
> → Tập dữ liệu cuối `datasets/final/` phục vụ huấn luyện và đánh giá
>
> **Tín hiệu ngữ cảnh:** ghép alt và desc của ảnh để hỗ trợ phân biệt logo, banner và ảnh không liên quan.
>
> **Checkpoint:** ghi tiến trình vào `processed_urls.txt` và `pending_images.jsonl` để có thể khôi phục pipeline khi bị gián đoạn.
>
> **Human-in-the-loop:** AI chỉ đề xuất nhãn; nhãn cuối cùng chỉ được chấp nhận sau bước kiểm duyệt thủ công.

### 2.3 Xây dựng truy vấn tìm kiếm theo ngữ cảnh tiếng Việt

Thay vì phụ thuộc vào các từ khóa tiếng Anh có sẵn, nhóm xây dựng bộ truy vấn tiếng Việt đặc thù cho từng nhãn nhằm tối đa hóa khả năng truy xuất hình ảnh từ các trang nông nghiệp trong nước (ví dụ: các cổng thông tin khuyến nông, website doanh nghiệp thuốc bảo vệ thực vật, blog kỹ thuật canh tác). Cụ thể, chiến lược tìm kiếm được định nghĩa dưới dạng ánh xạ nhãn → danh sách truy vấn, ví dụ:

**Bảng 2:** Trích lược bộ truy vấn tiếng Việt theo cây trồng và nhãn bệnh.

| Nhãn bệnh | Một số truy vấn tiêu biểu |
|-----------|--------------------------|
| **Lúa** | |
| BrownSpot | "Bệnh đốm nâu hại lúa", "triệu chứng đốm nâu lúa" |
| LeafBlast | "Bệnh đạo ôn hại lúa", "hình ảnh bệnh đạo ôn lúa" |
| Hispa | "Bọ gai hại lúa", "hình ảnh bọ gai lúa" |
| Healthy | "Lúa khỏe mạnh", "cây lúa phát triển tốt" |
| **Cà phê** | |
| LeafMiner | "Bệnh sâu vẽ bùa cà phê", "hình ảnh bệnh sâu vẽ bùa trên lá cà phê" |
| PowderyMildew | "Bệnh phấn trắng cà phê", "hình ảnh bệnh phấn trắng hại cà phê" |
| Rust | "Bệnh nấm rỉ sắt cà phê", "bệnh rỉ sắt hại cà phê", "hình ảnh bệnh gỉ sắt cà phê" |
| AlgalLeafSpot | "Bệnh đốm rong cà phê", "hình ảnh bệnh đốm rong trên lá cà phê" |

Với mỗi truy vấn, hệ thống gọi tối đa 50 kết quả trả về từ công cụ tìm kiếm và loại trùng ở mức URL, sau đó gắn nhãn tạm thời cho toàn bộ ảnh được cào từ URL đó dựa trên truy vấn sinh ra nó. Nhãn tạm này chỉ đóng vai trò gợi ý; việc xác định nhãn chính thức được thực hiện ở các giai đoạn sau.

### 2.4 Cào dữ liệu ảnh và ngữ cảnh văn bản

Để trích xuất ảnh từ các trang HTML có cấu trúc đa dạng, nhóm sử dụng thư viện **Crawl4AI** – một crawler bất đồng bộ được xây dựng trên Playwright, cho phép render trang như trình duyệt thật và trả về danh sách các phần tử đa phương tiện đã được chuẩn hóa. Với mỗi URL, quy trình thực hiện:

1. Khởi tạo phiên crawl thông qua `AsyncWebCrawler`; duyệt toàn bộ thẻ `<img>` và lọc bỏ các định dạng không phù hợp (`.svg`, `.gif`, `.ico`).
2. Tải ảnh gốc thông qua `httpx.AsyncClient` với User-Agent giả lập trình duyệt để tránh bị chặn bởi một số CDN.
3. Tạo cặp (ảnh, văn bản ngữ cảnh): văn bản được ghép từ thuộc tính `alt` và mô tả `desc` của ảnh – đây là tín hiệu ngôn ngữ quan trọng giúp bước tiền gán nhãn phân biệt những ảnh không liên quan (ví dụ: logo, banner quảng cáo).
4. Lưu ảnh với tên định danh duy nhất dạng `img_<uuid>.<ext>` ở folder `datasets/raw/scraped_data/images/<label>/` và văn bản ngữ cảnh tương ứng tại `datasets/raw/scraped_data/context/<label>/`.
5. Ghi URL records đã xử lý vào `processed_urls.txt`.

Số lượng tác vụ cào đồng thời được kiểm soát bằng `asyncio.Semaphore` với giá trị mặc định `MAX_CONCURRENT_SCRAPES = 5` nhằm cân bằng giữa tốc độ thu thập và mức độ "thân thiện" với máy chủ bên thứ ba.

### 2.5 Gán nhãn tự động bằng Gemma 4

Sau khi có kho ảnh thô, nhóm thực hiện bước tiền gán nhãn tự động nhằm giảm tải công việc cho giai đoạn kiểm duyệt thủ công. Ý tưởng cốt lõi là tận dụng khả năng đa phương thức của một VLM: thay vì chỉ nhìn vào ảnh như các mô hình phân loại thuần thị giác, mô hình cùng lúc quan sát ảnh và văn bản ngữ cảnh lấy từ trang web nguồn. Điều này đặc biệt hữu ích trong trường hợp ảnh mờ, nhiễu hoặc có nhiều đối tượng – những tình huống mà thông tin ngôn ngữ xung quanh ảnh đóng vai trò như tín hiệu phụ trợ.

Mô hình được sử dụng là **Gemma 4**, truy cập qua một OpenAI-compatible API endpoint. API endpoint này được nhóm triển khai trên Kaggle bằng llama.cpp và Unsloth. Prompt được thiết kế theo phong cách role-conditioned, ràng buộc đầu ra dưới dạng JSON:

```python
prompt_text = f""" You are an agricultural expert. Look at this image and
the surrounding text from a Vietnamese blog: "{context}".
Determine if this is a valid close-up of a rice plant. If it is, classify
it strictly as ONE of these four categories: Healthy, BrownSpot, Hispa,
or LeafBlast.
Respond ONLY with a JSON object in this format:
{{"prediction": "LabelName"}}. If it is not a valid image of a rice
plant, respond with {{"prediction": "Invalid"}}. """
```

*Listing 1: Trích đoạn prompt tiền gán nhãn cho ảnh lúa.*

Một số lưu ý kỹ thuật được nhóm áp dụng:

- Bật chế độ JSON (`response_format={"type": "json_object"}`) và đặt `temperature=0.1` để đầu ra có tính xác định, dễ parse và ít bị "ảo giác".
- Giới hạn tập nhãn ngay trong prompt, buộc mô hình rơi về nhãn `Invalid` khi ảnh không thuộc miền quan tâm – qua đó tự động loại bỏ logo, banner, ảnh minh họa không đúng cây trồng.
- Kiểm soát tải cho VLM bằng `MAX_CONCURRENT_AI = 2`. Vì mô hình chạy trên Kaggle T4 GPU có giới hạn bộ nhớ là 16GB, nên ta cần giới hạn bộ nhớ lại để tránh lỗi Cuda OOM.

Kết quả của bước này là một tệp JSONL, trong đó mỗi dòng mô tả một ảnh kèm theo trường `predictions` chứa nhãn do AI đề xuất.

### 2.6 Kiểm duyệt thủ công bằng công cụ gán nhãn tự xây dựng

Dù mô hình VLM đạt độ chính xác khá, nhãn do AI sinh ra vẫn không đủ tin cậy để trực tiếp dùng cho huấn luyện – đặc biệt ở những cặp bệnh dễ nhầm lẫn như BrownSpot và LeafBlast ở cây lúa. Vì vậy, nhóm phát triển một công cụ gán nhãn riêng bằng **Streamlit** nhằm hỗ trợ con người kiểm duyệt lại toàn bộ tập dữ liệu một cách hiệu quả.

Công cụ cung cấp các tính năng chính sau:

- Giao diện hai cột hiển thị đồng thời ảnh và các nút chọn nhãn (kèm tên tiếng Việt như "Đốm nâu", "Đạo ôn", "Gỉ sắt"), giúp người gán nhãn – ngay cả khi không phải chuyên gia – dễ dàng đối chiếu.
- Làm nổi bật gợi ý của AI (viền xanh) và nhãn do người chọn (nền xanh đậm), tạo ra một vòng phản hồi trực quan: người dùng chỉ cần xác nhận khi AI đúng, và chỉ can thiệp khi AI sai.
- Điều hướng bằng bàn phím (ArrowLeft/Right, phím số 1–9 để gán nhãn đồng thời chuyển sang ảnh kế tiếp), giúp tăng tốc quá trình gán nhãn lên nhiều lần so với thao tác chuột.
- Phát hiện ảnh trùng lặp bằng hàm băm MD5 và tự động đánh dấu là Invalid – loại bỏ nhiễu do các website nông nghiệp thường sử dụng lại ảnh của nhau.
- Công cụ chỉnh sửa nhẹ (xoay, cắt theo phần trăm cạnh) được tích hợp ngay trong ứng dụng để xử lý những ảnh bị xoay lệch hoặc có viền quảng cáo.
- Xuất dữ liệu dưới hai dạng: (i) tệp JSON chỉ chứa nhãn và (ii) tệp ZIP chứa cả ảnh và JSON với đường dẫn tương đối, thuận tiện cho việc chia sẻ giữa các thành viên nhóm.
- Chế độ Gallery cho phép quan sát tổng quan, lọc theo nhãn và nhảy nhanh tới các ảnh có kết quả đáng ngờ để kiểm tra lại.

### 2.7 Mở rộng sang bài toán segmentation với SAM 3

Do các ảnh được cào về có chứa rất nhiều lá, không giống với ảnh có sẵn trong hai bộ dataset. Do đó, nhóm mở rộng bài toán từ classification thành classification + segmentation để có thể nhận diện được nhiều lá bị bệnh trên cùng một bức ảnh. Để tránh chi phí gán mask thủ công, nhóm sử dụng mô hình **Segment Anything Model 3** để tạo ra pseudo-mask, sau đó refine thủ công để tạo ra mask cho quá trình huấn luyện. Pipeline hỗ trợ hai chế độ:

- **Promptable Concept Segmentation:** truyền trực tiếp prompt văn bản ("leaf") cùng các bounding box sẵn có để mô hình tạo ra mask cho các đối tượng tương ứng.
- **Click Segmentation:** sử dụng một điểm click (mặc định là tâm ảnh) làm prompt, phù hợp khi ảnh chỉ có một đối tượng chính.

Pseudo-mask được tạo ra sẽ được chuyển thành polygon bằng OpenCV và ghi thẳng vào tệp `annotations.coco.json` theo chuẩn COCO. Sau đó dữ liệu được chia làm 5 phần tương ứng 5 thành viên trong nhóm để refine lại kết quả của mô hình một cách thủ công.

### 2.8 Cấu trúc lưu trữ và tính toàn vẹn dữ liệu

Toàn bộ dữ liệu sau quy trình được tổ chức theo cây thư mục thống nhất, phân theo cây trồng và nhãn bệnh:

```
datasets/final/
  coffee_leaf_disease/
    0/ ......... LeafMiner (Bệnh sâu vẽ bùa)
    1/ ......... PowderyMildew (Bệnh phấn trắng)
    2/ ......... Rust (Bệnh nấm rỉ sắt)
    3/ ......... AlgalLeafSpot (Bệnh đốm rong)
    annotations.coco.json
  rice_leaf_disease/
    BrownSpot/
    Healthy/
    Hispa/
    LeafBlast/
    annotations.coco.json
```

Để đảm bảo tính toàn vẹn và khả năng tái lập, nhóm tuân thủ các nguyên tắc:

- **Tách biệt ảnh thô và ảnh đã gán nhãn:** thư mục `datasets/raw/` lưu toàn bộ ảnh cào về (kể cả ảnh bị loại), trong khi `datasets/final/` chỉ chứa các ảnh đã được con người xác nhận.
- **Giữ lại source metadata:** mỗi ảnh đi kèm tệp văn bản ghi Source URL và đoạn ngữ cảnh gốc, hỗ trợ việc truy vết và tuân thủ bản quyền.
- **Hỗ trợ khôi phục:** mọi bước có trạng thái (scraping, classification) đều ghi lại tiến trình vào checkpoint, cho phép chạy lại nhiều lần mà không gây mất dữ liệu, trùng lặp.

### 2.9 Thảo luận và hạn chế

Pipeline trên có một số ưu điểm đáng chú ý: (i) giảm đáng kể công sức thu thập và gán nhãn nhờ kết hợp tìm kiếm – cào web - gán nhãn tự động bằng VLM; (ii) đảm bảo được tính đặc thù địa lý do sử dụng truy vấn tiếng Việt; (iii) duy trì được quyền kiểm soát chất lượng cuối cùng thông qua bước human-in-the-loop. Tuy nhiên, nhóm cũng ghi nhận những hạn chế cần khắc phục ở các giai đoạn sau của đồ án:

- **Thiên lệch nguồn (source bias):** nhiều ảnh được lấy từ cùng một vài cổng thông tin nông nghiệp lớn, dẫn tới sự đồng nhất về phong cách chụp và có thể làm giảm khả năng tổng quát hóa của mô hình.
- **Chênh lệch số lượng giữa các lớp:** nhãn Healthy và các bệnh phổ biến (đạo ôn, gỉ sắt) có xu hướng chiếm ưu thế so với Hispa hay nhện đỏ. Vấn đề mất cân bằng dữ liệu này sẽ được xử lý ở giai đoạn tiền xử lý và huấn luyện.
- **Sai số của bước gán nhãn:** Vì dữ liệu được gán nhãn thủ công không có chuyên gia, nên sẽ có sai sót.
- **Vấn đề bản quyền:** dữ liệu chỉ được sử dụng cho mục đích nghiên cứu, học thuật và không được phân phối lại; mọi ảnh đều giữ lại thông tin URL nguồn nhằm đảm bảo tính truy vết.

---

## 3 Phân tích khám phá dữ liệu (EDA)

### 3.1 Thách thức của tập dữ liệu nông nghiệp

Trước khi triển khai các mô hình học sâu, cần nhận diện rõ các thách thức bản chất của dữ liệu ảnh lá cây thu thập ngoài thực địa. Các thách thức này không chỉ ảnh hưởng đến chất lượng đặc trưng và mức độ tổng quát hóa của mô hình, mà còn là cơ sở để chuyển từ EDA sang các quyết định tiền xử lý và huấn luyện.

**Biến thiên điều kiện chụp ảnh:** ảnh được ghi nhận bằng điện thoại trong điều kiện ánh sáng tự nhiên không kiểm soát, dẫn đến thay đổi mạnh về độ sáng, cân bằng trắng, góc chụp, khoảng cách và nền ảnh.

**Mất cân bằng lớp:** số lượng mẫu giữa các lớp bệnh không đồng đều, khiến mô hình dễ thiên lệch về lớp đa số nếu chỉ tối ưu Accuracy.

**Tương đồng triệu chứng giai đoạn sớm:** các cặp lớp như BrownSpot–LeafBlast (lúa) và AlgalLeafSpot–Rust (cà phê) có biểu hiện màu sắc/hình thái gần nhau, làm tăng xác suất nhầm lẫn.

**Domain shift giữa hai miền dữ liệu:** dữ liệu lúa và cà phê có khác biệt đáng kể về hình thái lá và phân phối màu nền, làm tăng độ khó khi huấn luyện một mô hình thống nhất.

**Vùng bệnh nhỏ so với toàn ảnh:** annotation COCO cho thấy nhiều vùng bệnh chiếm tỉ lệ nhỏ trong ảnh; phần lớn pixel thuộc nền lá khỏe, gây nhiễu cho bài toán phân loại.

**Nhận xét:** Đây là bộ dữ liệu có tính thực tế cao. Vì vậy, các tiểu mục EDA tiếp theo được trình bày theo cùng một logic: thống kê đặc trưng dữ liệu, rút ra insight, chỉ ra ảnh hưởng tới mô hình và từ đó làm rõ quyết định kỹ thuật tương ứng.

### 3.2 Tổng quan tập dữ liệu

Tập dữ liệu gồm hai domain độc lập: lúa và cà phê, được lưu dưới định dạng COCO. Bảng 3 tổng hợp các thống kê nền tảng được sử dụng xuyên suốt phần EDA.

**Bảng 3:** Thống kê tổng quan theo domain

| Chỉ số | Lúa | Cà phê | Tổng |
|--------|-----|--------|------|
| Số lớp | 4 | 4 | 8 |
| Số ảnh | 3,421 | 3,879 | 7,300 |
| Số annotation COCO | 3,720 | 3,842 | 7,562 |
| Width trung bình (px) | 2,031 | 971 | – |
| Height trung bình (px) | 2,026 | 1,154 | – |
| Imbalance Ratio (IR) | 2.77x | 5.28x | – |
| CV theo lớp | 52.1% | 51.8% | – |
| Annotation trên mỗi ảnh | 1.09 (min=1, max=28) | 1.00 (min=1, max=1) | – |

**Bảng 4:** Phân phối lớp chi tiết của tập dữ liệu

| Lớp | Số ảnh | Tỉ lệ (%) |
|-----|--------|-----------|
| **Lúa** | | |
| Healthy | 1,503 | 43.9 |
| LeafBlast | 793 | 23.2 |
| Hispa | 583 | 17.0 |
| BrownSpot | 542 | 15.8 |
| **Cà phê** | | |
| Rust | 1,416 | 36.5 |
| LeafMiner | 1,226 | 31.6 |
| AlgalLeafSpot | 969 | 25.0 |
| PowderyMildew | 268 | 6.9 |

**Nhận xét:** Bảng tổng quan cho thấy hai domain khác nhau không chỉ ở số lượng ảnh mà còn ở kích thước ảnh, mức mất cân bằng lớp và cấu trúc annotation. Vì vậy, các phân tích tiếp theo được thực hiện theo từng domain rồi mới đối chiếu chéo. Lưu ý rằng các số liệu width/height và annotation được đo trên toàn bộ tập dữ liệu, còn các thống kê màu sắc ở tiểu mục "Phân tích độ sáng và kênh màu RGB" được tính trên mẫu 50 ảnh/lớp.

### 3.3 Phân phối lớp dữ liệu

**Định nghĩa 3.1** (Imbalance Ratio và Coefficient of Variation). Với phân phối số mẫu theo lớp $\{N_c\}_{c=1}^{|C|}$, hai chỉ số định lượng mức độ mất cân bằng được sử dụng trong báo cáo là

$$IR = \frac{N_{majority}}{N_{minority}} \tag{3.1}$$

và

$$CV = \frac{\sigma_N}{\mu_N} \times 100\% \tag{3.2}$$

Trong đó $N_{majority}$ và $N_{minority}$ lần lượt là số mẫu của lớp đa số và lớp thiểu số; $\sigma_N$ là độ lệch chuẩn số mẫu giữa các lớp và $\mu_N$ là giá trị trung bình số mẫu.

Theo (3.1) và (3.2), IR cho biết mức chênh lệch giữa lớp lớn nhất và lớp nhỏ nhất, còn CV phản ánh độ phân tán của toàn bộ phân phối lớp. Đây là hai chỉ số ngắn gọn nhưng đủ trực quan để hỗ trợ lựa chọn metric đánh giá và chiến lược cân bằng dữ liệu.

**Bảng 5:** Chỉ số mất cân bằng lớp theo domain

| Domain | IR | CV | Lớp đa số | Lớp thiểu số |
|--------|----|----|-----------|--------------|
| Lúa | 2.77x | 52.1% | Healthy (1,503) | BrownSpot (542) |
| Cà phê | 5.28x | 51.8% | Rust (1,416) | PowderyMildew (268) |

**Hình 2:** Phân phối lớp dữ liệu của hai domain (biểu đồ cột và biểu đồ tròn).

**Insight rút ra:** Hình 2 cho thấy sự mất cân bằng lớp xuất hiện ở cả hai domain và rõ rệt hơn ở domain cà phê. Lớp PowderyMildew chỉ chiếm 6.9% trong khi Rust đạt 36.5%, tức chênh lệch hơn 5 lần; ở domain lúa, Healthy cũng chiếm ưu thế rõ rệt so với BrownSpot.

**Ảnh hưởng tới mô hình:** Với cấu trúc này, mô hình dễ đạt Accuracy bề ngoài cao nhờ thiên về lớp đa số nhưng vẫn bỏ sót các lớp ít mẫu, đặc biệt khi đánh giá chỉ dựa trên một chỉ số tổng quát.

**Quyết định kỹ thuật:** Ở giai đoạn huấn luyện, cần kết hợp các cơ chế giảm lệch lớp như WeightedRandomSampler, class-weighted loss hoặc focal loss; ở giai đoạn đánh giá, cần ưu tiên Macro-F1, confusion matrix và F1 theo từng lớp thay vì chỉ báo cáo Accuracy.

### 3.4 Phân tích kích thước và tỉ lệ ảnh

Độ phân giải và tỉ lệ khung hình đa dạng tạo ra thách thức trực tiếp cho bước chuẩn hóa đầu vào. Trong phân tích này, tỉ lệ khung hình được tính theo

$$AR = \frac{W}{H} \tag{3.3}$$

trong đó AR = 1 tương ứng ảnh gần vuông, AR > 1 là ảnh ngang và AR < 1 là ảnh dọc. Từ công thức này có thể thấy rằng nếu ép mọi ảnh về cùng một kích thước vuông mà không giữ tỉ lệ, biến dạng hình học sẽ xuất hiện rõ nhất ở các ảnh có AR lệch xa 1.

Trong thực tế, ảnh lúa có xu hướng gần vuông nhiều hơn, trong khi ảnh cà phê xuất hiện nhiều ảnh dọc hoặc lệch tỉ lệ hơn.

**Bảng 6:** Thống kê hình học ảnh

| Chỉ số | Lúa | Cà phê |
|--------|-----|--------|
| Width range (px) | [132, 3120] | [163, 4000] |
| Height range (px) | [206, 3120] | [168, 2250] |
| AR range | [0.57, 2.71] | [0.45, 2.61] |
| Mean width (px) | 2,031 | 971 |
| Median width (px) | 1,903 | 907 |
| Mean AR | 1.01 | 0.86 |

**Hình 3:** Phân tích kích thước ảnh gồm: tương quan Width–Height, phân phối chiều rộng và phân phối aspect ratio.

**Insight rút ra:** Hình 3 cho thấy ảnh có độ phân tán lớn về kích thước và tỉ lệ, đặc biệt ở domain cà phê (AR trung bình 0.86, thiên về ảnh dọc) so với lúa (AR trung bình 1.01, gần vuông).

**Ảnh hưởng tới mô hình:** Nếu chuẩn hóa bằng resize cứng về ảnh vuông, mô hình có thể học từ hình dạng đã bị méo hoặc mất chi tiết ở vùng tổn thương nhỏ, nhất là với các ảnh lệch tỉ lệ nhiều.

**Quyết định kỹ thuật:** Quy trình phù hợp hơn là padding giữ tỉ lệ trước, sau đó mới resize/crop về kích thước làm việc. Lựa chọn canvas 256×256 rồi crop 224×224 giúp cân bằng giữa chi phí tính toán và nhu cầu bảo toàn đặc trưng hình thái.

### 3.5 Phân tích độ sáng và kênh màu RGB

Để lượng hóa khác biệt quang học giữa các domain và giữa các lớp, báo cáo sử dụng độ sáng cảm nhận

$$L(i,j) = 0.299R(i,j) + 0.587G(i,j) + 0.114B(i,j) \tag{3.4}$$

theo chuẩn BT.601, trung bình độ sáng

$$\mu_L(I) = \frac{1}{H \cdot W} \sum_{i=1}^{H} \sum_{j=1}^{W} L(i,j) \tag{3.5}$$

và độ tương phản xấp xỉ

$$\sigma_L(I) = \sqrt{\frac{1}{H \cdot W} \sum_{i=1}^{H} \sum_{j=1}^{W} (L(i,j) - \mu_L(I))^2} \tag{3.6}$$

Các hệ số 0.299, 0.587 và 0.114 phản ánh mức độ nhạy sáng khác nhau của thị giác người với từng kênh màu; trong đó kênh xanh lá có trọng số lớn nhất. Nhóm thống kê này được giữ lại vì chúng đủ gọn để mô tả khác biệt ánh sáng và phục vụ trực tiếp cho việc chọn chiến lược chuẩn hóa theo kênh và augmentation quang học.

**Bảng 7:** Thống kê độ sáng và tương phản theo lớp (mẫu 50 ảnh/lớp)

| Lớp | Brightness mean | Brightness std | Contrast mean | Contrast std |
|-----|----------------|----------------|---------------|--------------|
| **Domain Lúa** | | | | |
| BrownSpot | 201.26 | 17.55 | 44.85 | 9.45 |
| Healthy | 201.44 | 11.86 | 50.20 | 9.20 |
| Hispa | 200.37 | 20.24 | 43.83 | 10.20 |
| LeafBlast | 194.92 | 21.70 | 45.02 | 12.70 |
| **Domain Cà phê** | | | | |
| LeafMiner | 127.88 | 11.84 | 52.62 | 6.25 |
| Rust | 128.14 | 10.97 | 51.71 | 4.63 |
| AlgalLeafSpot | 119.18 | 13.52 | 56.27 | 5.61 |
| PowderyMildew | 117.47 | 8.25 | 57.26 | 4.57 |

*Ghi chú: "độ sáng trung bình" trong báo cáo được tính trên mẫu thống kê (N=50 ảnh/lớp, tổng 200 ảnh mỗi domain), không lấy từ bảng tổng quan kích thước ảnh.*

**Hình 4:** Phân phối độ sáng, giá trị trung bình RGB và độ tương phản theo lớp bệnh.

**Insight rút ra:** Hình 4 phản ánh khác biệt quang học rõ ràng giữa hai domain: độ sáng trung bình của lúa cao hơn đáng kể so với cà phê (xấp xỉ 199.5 so với 123.2 theo mẫu thống kê). Đồng thời, độ tương phản giữa các lớp cũng biến thiên mạnh.

**Ảnh hưởng tới mô hình:** Nhiễu chiếu sáng và khác biệt RGB theo domain có thể làm mô hình học quá nhiều vào điều kiện chụp thay vì tín hiệu bệnh, từ đó làm giảm độ bền vững khi triển khai trên ảnh thực địa mới.

**Quyết định kỹ thuật:** Cần chuẩn hóa theo kênh dựa trên thống kê của tập huấn luyện và bổ sung augmentation quang học như brightness/contrast/saturation để tăng khả năng thích nghi với thay đổi điều kiện chụp thực tế.

### 3.6 Trực quan hóa mẫu bệnh

Quan sát thủ công các mẫu ảnh theo từng lớp là bước bổ sung cho thống kê định lượng, giúp nhận diện đặc trưng hình thái bệnh và phát hiện các ca khó như ảnh mờ, chồng lá, góc chụp xiên, triệu chứng ở giai đoạn sớm hoặc nền nhiễu mạnh.

**Hình 5:** Lưới mẫu ảnh bệnh của hai domain.

**Hình 6:** Lưới mẫu ảnh bệnh của hai domain.

**Insight rút ra:** Hình 5 và Hình 6 cho thấy dữ liệu có tính thực địa cao, với khác biệt lớn về nền ảnh, góc chụp, khoảng cách, độ nét và mức độ biểu hiện triệu chứng.

**Ảnh hưởng tới mô hình:** Đây là tín hiệu tốt về tính đại diện của dữ liệu, nhưng cũng làm tăng độ khó tổng quát hóa. Nếu chỉ dùng kiến trúc đơn giản hoặc augmentation nhẹ, mô hình dễ học theo bối cảnh nền thay vì học đúng đặc trưng bệnh.

**Quyết định kỹ thuật:** Cần ưu tiên augmentation hình học và quang học có kiểm soát, đồng thời theo dõi lỗi theo từng lớp để phát hiện sớm nhóm mẫu khó hoặc các lớp bị ảnh hưởng mạnh bởi bối cảnh nền.

### 3.7 Phân tích annotation COCO

Phân tích annotation tập trung vào ba yếu tố: số annotation trên mỗi ảnh, tỉ lệ diện tích vùng bệnh trên toàn ảnh và phân phối kích thước vùng bệnh. Một đại lượng quan trọng là

$$r_{area} = \frac{A_{bbox}}{W \cdot H} \tag{3.7}$$

trong đó $A_{bbox}$ là diện tích bounding box của vùng bệnh, còn $W \cdot H$ là diện tích toàn ảnh. Khi chuẩn hóa ảnh về kích thước $S \times S$, số pixel biểu diễn tổn thương sau resize xấp xỉ tỷ lệ với $r_{area} S^2$; vì vậy, các vùng bệnh nhỏ là nhóm dễ mất chi tiết nhất khi giảm độ phân giải.

**Bảng 8:** Thống kê annotation quan trọng

| Chỉ số | Lúa | Cà phê |
|--------|-----|--------|
| Annotation/ảnh trung bình | 1.09 | 1.00 |
| Annotation/ảnh nhỏ nhất | 1 | 1 |
| Annotation/ảnh lớn nhất | 28 | 1 |
| Đặc điểm vùng bệnh | Nhiều vùng nhỏ, phân tán | Nhiều trường hợp một vùng chính |

**Hình 7:** Phân tích annotation COCO: số annotation trên mỗi ảnh, tỉ lệ BBox/ảnh và phân phối log(BBox Area + 1).

**Insight rút ra:** Hình 7 cho thấy phần lớn ảnh có số annotation thấp, nhưng domain lúa vẫn tồn tại các trường hợp nhiều vùng tổn thương (tối đa 28 annotation/ảnh). Đồng thời, phân bố diện tích vùng bệnh thiên về các giá trị nhỏ, nghĩa là tổn thương thường chỉ chiếm một phần nhỏ so với toàn ảnh.

**Ảnh hưởng tới mô hình:** Đây là nguyên nhân quan trọng khiến mô hình dễ bỏ sót bệnh sau bước resize hoặc khi backbone chủ yếu nhìn tín hiệu toàn cục của lá và nền ảnh.

**Quyết định kỹ thuật:** Về thực hành, cần chọn kích thước đầu vào đủ lớn, tránh các phép crop quá mạnh ở đầu pipeline và ưu tiên kiến trúc/chiến lược học có khả năng khai thác đặc trưng cục bộ hoặc đa tỉ lệ để cải thiện nhận diện tổn thương nhỏ.

### 3.8 Nhận diện cặp bệnh dễ nhầm lẫn

Để định lượng mức chồng lấp màu giữa các lớp dễ nhầm, báo cáo sử dụng histogram RGB chuẩn hóa cho từng kênh

$$h_c(v) = \frac{1}{H \cdot W} \sum_{i=1}^{H} \sum_{j=1}^{W} \mathbf{1}[I_c(i,j) = v], \quad v \in \{0, \ldots, 255\} \tag{3.8}$$

và khoảng cách Bhattacharyya

$$D_B(p, q) = -\ln \left( \sum_{v=0}^{255} \sqrt{p(v)q(v)} \right) \tag{3.9}$$

Trong ngữ cảnh này, giá trị $D_B$ càng nhỏ thì mức chồng lấp màu càng lớn. Phân tích tập trung vào hai cặp dễ nhầm là BrownSpot–LeafBlast và AlgalLeafSpot–Rust.

**Bảng 9:** Khoảng cách Bhattacharyya theo kênh màu cho các cặp dễ nhầm

| Cặp lớp | Kênh R | Kênh G | Kênh B |
|---------|--------|--------|--------|
| BrownSpot vs LeafBlast | 0.076 | 0.051 | 0.054 |
| AlgalLeafSpot vs Rust | 0.004 | 0.009 | 0.009 |

**Hình 8:** So sánh histogram RGB trên các cặp bệnh dễ nhầm lẫn.

**Insight rút ra:** Ở Hình 8, các đường histogram giữa hai lớp trong từng cặp có mức chồng lấp cao, đặc biệt với AlgalLeafSpot–Rust (khoảng cách Bhattacharyya chỉ 0.004, 0.009 và 0.009 trên ba kênh RGB).

**Ảnh hưởng tới mô hình:** Kết quả này cho thấy màu sắc toàn cục không đủ để tách lớp ổn định ở nhóm bệnh gần nhau; nếu chỉ dựa trên tín hiệu màu, mô hình dễ nhầm lẫn ở các giai đoạn bệnh có biểu hiện tương tự.

**Quyết định kỹ thuật:** Cần ưu tiên mô hình học tốt đặc trưng texture và hình thái cục bộ, chẳng hạn backbone mạnh hơn, attention theo vùng hoặc chiến lược đặc trưng đa tỉ lệ. Trong đánh giá, cần theo dõi confusion matrix riêng cho các cặp lớp này thay vì chỉ nhìn điểm số tổng hợp.

### 3.9 Chỉ số đánh giá Macro F1-score

**Định nghĩa 3.2** (Macro F1-score). Với tập C lớp, chỉ số Macro-F1 được định nghĩa bởi

$$\text{Macro-F1} = \frac{1}{|C|} \sum_{c=1}^{|C|} F1_c \tag{3.10}$$

trong đó

$$F1_c = \frac{2P_c R_c}{P_c + R_c}, \quad P_c = \frac{TP_c}{TP_c + FP_c}, \quad R_c = \frac{TP_c}{TP_c + FN_c} \tag{3.11}$$

Ở đây, $TP_c$, $FP_c$, $FN_c$ lần lượt là số dự đoán đúng dương tính, dương tính giả và âm tính giả của lớp $c$.

Macro-F1 lấy trung bình không trọng số trên các lớp, nên mọi lớp đều có mức ảnh hưởng ngang nhau trong đánh giá tổng thể. Điều này phù hợp trực tiếp với bài toán hiện tại, nơi cả hai domain đều có lệch lớp đáng kể.

Một lập luận định lượng để ưu tiên Macro-F1 là xét bộ phân loại luôn dự đoán mọi mẫu vào lớp đa số $c^*$ có tỉ lệ xuất hiện $\pi^*$. Khi đó Accuracy bằng $\pi^*$, còn Macro-F1 bằng

$$\text{Macro-F1} = \frac{1}{|C|} \cdot \frac{2\pi^*}{1 + \pi^*} \tag{3.12}$$

vì chỉ lớp đa số có F1 khác 0 còn các lớp còn lại đều bị bỏ sót hoàn toàn. Công thức này cho thấy Accuracy có thể vẫn tương đối cao trong tập lệch lớp, trong khi Macro-F1 phạt mạnh các mô hình bỏ quên lớp thiểu số.

**Quyết định đánh giá:** Nên báo cáo đồng thời Macro-F1, confusion matrix, F1 theo từng lớp và lỗi theo domain để tránh kết luận thiên lệch từ một chỉ số duy nhất.

### 3.10 Tóm tắt phát hiện và quyết định kỹ thuật

**Bảng 10:** Tóm tắt các phát hiện chính từ EDA

| Khía cạnh | Lúa | Cà phê |
|-----------|-----|--------|
| Tổng số ảnh | 3,421 | 3,879 |
| Số lớp | 4 lớp | 4 lớp |
| Imbalance Ratio (IR) | 2.77x (Healthy trội hơn) | 5.28x (Rust trội hơn) |
| Kích thước ảnh | 132–3120 px, xu hướng vuông | 163–4000 px, nhiều ảnh dọc |
| Độ sáng (theo mẫu 50 ảnh/lớp) | Mean ~199.5 | Mean ~123.2 |
| Cặp dễ nhầm | BrownSpot ↔ LeafBlast | AlgalLeafSpot ↔ Rust |
| Annotation/ảnh | 1.09 (min=1, max=28) | 1.00 (min=1, max=1) |

Từ các phát hiện trên, các quyết định kỹ thuật cho giai đoạn preprocessing/training gồm:

- **Mất cân bằng lớp:** áp dụng WeightedRandomSampler, class-weighted loss hoặc focal loss; đồng thời dùng Macro-F1 và F1 theo lớp làm trục đánh giá chính.
- **Hình học ảnh đa dạng:** chuẩn hóa về canvas 256×256 theo padding giữ tỉ lệ, sau đó crop 224×224 để hạn chế méo hình và vẫn giữ chi phí huấn luyện ở mức hợp lý.
- **Biến thiên quang học:** tính mean/std từ train split và áp dụng ColorJitter (brightness=0.3, contrast=0.3, saturation=0.2) cùng các phép biến đổi hình học như flip ngang/dọc, RandomRotation (±30°).
- **Vùng bệnh nhỏ và phân tán:** tránh resize/crop quá mạnh ở đầu pipeline, giữ kích thước đầu vào đủ lớn và ưu tiên mô hình có khả năng khai thác đặc trưng cục bộ hoặc đa tỉ lệ.
- **Cặp bệnh dễ nhầm và lệch miền:** theo dõi confusion matrix theo cặp lớp/domain và ưu tiên backbone hoặc cơ chế attention giúp phân biệt texture/hình thái tốt hơn đặc trưng màu toàn cục.

Tổng kết, EDA vẫn giữ được chiều sâu học thuật ở những chỗ cần thiết như định nghĩa chỉ số mất cân bằng và lập luận lựa chọn Macro-F1, nhưng trọng tâm được chuyển về phân tích dữ liệu thực tế và hệ quả kỹ thuật. Nhờ đó, phần này đóng vai trò như một cầu nối rõ ràng từ quan sát dữ liệu sang thiết kế pipeline tiền xử lý, chiến lược huấn luyện và cách đánh giá mô hình ở giai đoạn tiếp theo.

---

## 4 Tiền xử lý dữ liệu

### 4.1 Xây dựng bảng metadata hợp nhất từ dữ liệu thô

Quy trình tiền xử lý bắt đầu bằng việc hợp nhất toàn bộ ảnh từ hai domain vào một bảng metadata thống nhất. Bảng này đóng vai trò như lớp điều phối của toàn bộ pipeline: các bước làm sạch, chia tập, xuất ảnh và lưu cấu hình đều được thực hiện trên cùng một thực thể dữ liệu thay vì thao tác trực tiếp trên cấu trúc thư mục nguồn.

**Định nghĩa 4.1** (Bảng metadata hợp nhất). Mỗi mẫu ảnh được biểu diễn bởi một bộ metadata

$$m_i = (\text{sample\_id}_i, \text{domain}_i, \text{label}_i, \text{path}_i, W_i, H_i, \text{is\_valid}_i) \tag{4.1}$$

trong đó $\text{sample\_id}_i$ là định danh mẫu, $\text{domain}_i$ là miền dữ liệu, $\text{label}_i$ là nhãn bệnh, $\text{path}_i$ là đường dẫn tệp, $(W_i, H_i)$ là kích thước ảnh và $\text{is\_valid}_i$ là trạng thái hợp lệ. Tập metadata hợp nhất được ký hiệu là $M = \{m_i\}_{i=1}^{N}$.

Thiết kế này được chọn vì dữ liệu lúa và cà phê có cấu trúc lưu trữ khác nhau, trong khi các bước phía sau lại cần cùng một giao diện truy cập. Một phương án thay thế là duyệt thư mục trực tiếp ở từng bước xử lý; tuy nhiên, cách đó dễ phát sinh sai khác logic giữa các script, khó kiểm toán và kém tái lập. Metadata tập trung làm tăng thêm một tầng quản lý, nhưng đổi lại nó giúp chuẩn hóa đầu vào, lưu vết toàn bộ quyết định tiền xử lý và giảm rủi ro sai sót thủ công khi làm việc với nhiều nguồn dữ liệu.

**Bảng 11:** Thống kê số ảnh và kích thước trung bình theo lớp trước làm sạch

| Domain | Label | n_images | mean_width | mean_height |
|--------|-------|----------|------------|-------------|
| coffee | LeafMiner | 1226 | 986.9 | 1149.4 |
| coffee | Rust | 1416 | 966.6 | 1163.7 |
| coffee | AlgalLeafSpot | 969 | 963.1 | 1140.4 |
| coffee | PowderyMildew | 268 | 943.3 | 1179.2 |
| rice | BrownSpot | 542 | 2136.1 | 2133.3 |
| rice | Healthy | 1503 | 2101.3 | 2097.6 |
| rice | Hispa | 583 | 2080.3 | 2066.7 |
| rice | LeafBlast | 793 | 1791.4 | 1788.3 |

**Nhận xét:** Phân bố ban đầu cho thấy hai nguồn dữ liệu không chỉ lệch lớp mà còn khác biệt rõ về kích thước ảnh. Điều này hàm ý rằng nếu pipeline không được chuẩn hóa ngay từ đầu, mô hình có thể vô tình khai thác các đặc trưng phụ như độ phân giải hay bố cục ảnh để suy ra domain, thay vì học tín hiệu bệnh. Vì vậy, metadata hợp nhất không chỉ là công cụ quản trị dữ liệu mà còn là cơ chế kiểm soát tính nhất quán của toàn bộ quy trình tiền xử lý.

### 4.2 Làm sạch dữ liệu: invalid, duplicate, blurry

Sau bước hợp nhất metadata, dữ liệu được sàng lọc theo ba dạng nhiễu có ảnh hưởng trực tiếp đến quá trình học biểu diễn: tệp ảnh không hợp lệ, ảnh trùng nội dung và ảnh mờ. Trong ba nhóm này, blur là trường hợp khó xử lý nhất vì không tồn tại một ngưỡng tuyệt đối phù hợp cho mọi nguồn ảnh ngoài thực địa.

**Định nghĩa 4.2** (Tiêu chí làm sạch dữ liệu). Với mỗi ảnh ứng viên $I$, ba tiêu chí làm sạch được sử dụng như sau. Ảnh **invalid** là ảnh không thể mở hợp lệ (corrupt hoặc sai định dạng) và cần loại bỏ hoàn toàn. Ảnh **duplicate** được phát hiện bằng hàm băm MD5

$$h_{md5}(I) = MD5(\text{file\_bytes}(I)) \tag{4.2}$$

và hai ảnh được xem là trùng nội dung nếu có cùng giá trị $h_{md5}$. Đối với ảnh **blurry**, chỉ số Variance of Laplacian (VoL) được tính từ toán tử Laplacian rời rạc

$$L(x,y) = -4I(x,y) + I(x-1,y) + I(x+1,y) + I(x,y-1) + I(x,y+1) \tag{4.3}$$

và blur score tương ứng

$$\text{VoL}(I) = \frac{1}{N} \sum_{x,y} \left(L(x,y) - \bar{L}\right)^2 \tag{4.4}$$

trong đó $N$ là số điểm ảnh của ảnh sau khi áp dụng Laplacian. Giá trị $\text{VoL}(I)$ thấp biểu thị ảnh mờ, còn giá trị cao cho thấy ảnh chứa nhiều chi tiết cạnh hơn.

**Lý do lựa chọn và đánh đổi:** Ngưỡng blur được xác định theo quantile thấp (q = 0.02) của phân phối VoL, thay vì dùng một threshold cố định. Lý do là giá trị VoL phụ thuộc mạnh vào độ phân giải, khoảng cách chụp, cấu trúc texture của lá và khác biệt giữa hai domain; một ngưỡng tuyệt đối có thể loại quá tay ở domain ít chi tiết nhưng lại quá lỏng ở domain còn lại. Cách tiếp cận theo quantile giúp pipeline thích nghi với phân phối thực nghiệm và chỉ loại phần đuôi trái — tức nhóm ảnh mờ nhất tương đối của chính tập dữ liệu. Alternative gồm ngưỡng cố định được hiệu chỉnh thủ công theo từng domain hoặc các chỉ số chất lượng ảnh học sâu; tuy nhiên, các phương án này hoặc kém ổn định khi dữ liệu thay đổi, hoặc làm tăng độ phức tạp và giảm tính giải thích. Đánh đổi của quantile là nó kiểm soát tốt tỉ lệ loại bỏ hơn là một mức chất lượng tuyệt đối; vì vậy, nghiên cứu này chọn chiến lược bảo thủ: loại nhiễu nặng nhưng giữ tối đa các trường hợp khó vốn có giá trị cho khả năng tổng quát hóa.

**Bảng 12:** Tổng hợp kết quả làm sạch dữ liệu

| reason | count | ratio_percent |
|--------|-------|---------------|
| invalid | 0 | 0.00 |
| duplicate | 1 | 0.01 |
| blurry | 150 | 2.05 |
| kept | 7149 | 97.93 |

**Bảng 13:** Phân bố số ảnh theo lớp sau khi làm sạch

| domain | label | n_images |
|--------|-------|----------|
| coffee | LeafMiner | 1200 |
| coffee | Rust | 1387 |
| coffee | AlgalLeafSpot | 949 |
| coffee | PowderyMildew | 262 |
| rice | BrownSpot | 531 |
| rice | Healthy | 1472 |
| rice | Hispa | 571 |
| rice | LeafBlast | 777 |

**Nhận xét:** Kết quả làm sạch cho thấy dữ liệu nguồn gần như không có vấn đề hệ thống về tệp hỏng hay trùng lặp; nhiễu chủ đạo nằm ở chất lượng quang học của ảnh. Đây là một insight quan trọng, vì nó cho thấy thách thức của bài toán không nằm ở việc dọn lỗi cơ học trong dữ liệu, mà ở việc kiểm soát chất lượng tín hiệu đầu vào mà vẫn giữ được tính thực địa của tập ảnh.

**Hình 9:** Biểu đồ phân bố blur score theo domain và ngưỡng lọc mờ toàn cục (q=0.02).

**Nhận xét:** Hình 9 cho thấy ngưỡng lọc toàn cục q = 0.02 (8.3284) chỉ can thiệp vào phần đuôi trái của phân phối blur score và vẫn giữ lại 97.93% dữ liệu. Điều này đặc biệt quan trọng với ảnh thu thập ngoài thực địa: nếu làm sạch quá mạnh, pipeline có thể vô tình loại bỏ cả những trường hợp khó nhưng hợp lệ, làm cho tập huấn luyện trở nên "đẹp" hơn thực tế và khiến kết quả mô hình lạc quan giả tạo.

### 4.3 Chia dữ liệu chống leakage (Stratified Split)

Dữ liệu sau làm sạch được chia theo tỉ lệ 70% train, 15% validation, 15% test và stratify theo tổ hợp domain + label. Sau khi chia, quy trình kiểm tra overlap theo cả sample_id và md5 để đảm bảo không rò rỉ dữ liệu giữa các split.

**Định nghĩa 4.3** (Chia dữ liệu phân tầng chống leakage). Cho tập dữ liệu $D$ với nhãn tầng $s(i) = (\text{domain}_i, \text{label}_i)$. Phép chia train/val/test được gọi là phân tầng nếu, với mọi tầng $k$,

$$\frac{|D^k_{train}|}{|D_{train}|} \approx \frac{|D^k|}{|D|} \tag{4.5}$$

và đồng thời thỏa điều kiện chống leakage

$$S_a \cap S_b = \emptyset, \quad H_a \cap H_b = \emptyset, \quad a \neq b \in \{\text{train, val, test}\} \tag{4.6}$$

trong đó $S_a$ là tập sample_id và $H_a$ là tập hash MD5 thuộc split $a$.

**Lý do lựa chọn và đánh đổi:** Việc stratify theo tổ hợp domain + label được ưu tiên hơn stratify chỉ theo nhãn vì bài toán hiện tại đồng thời chứa lệch lớp và lệch miền. Nếu chỉ bảo toàn tần suất nhãn toàn cục, một split vẫn có thể vô tình lệch về thành phần domain, từ đó làm sai khác độ khó giữa train, validation và test. Một alternative mạnh hơn là group split theo cây, lô canh tác, thời điểm chụp hoặc thiết bị; cách đó kiểm soát leakage ở mức nguồn sinh dữ liệu tốt hơn, nhưng bộ dữ liệu hiện tại không cung cấp metadata tương ứng. Do vậy, kiểm tra đồng thời sample_id và MD5 là mức kiểm soát leakage khả thi và đủ chặt trong bối cảnh hiện có.

Để đạt đúng tỉ lệ toàn cục 70/15/15 mà vẫn giữ stratification ổn định, quy trình thực hiện tách hai bước: trước hết lấy 70% cho train và 30% cho tập tạm, sau đó chia đều tập tạm thành validation và test. Cách làm này đơn giản, minh bạch và dễ tái lập; lợi ích của các thủ tục chia ba nhánh phức tạp hơn không đủ lớn để biện minh cho chi phí triển khai tăng thêm trong bài toán hiện tại.

**Kết quả kiểm tra leakage:**

- sample_id train-val = 0, train-test = 0, val-test = 0.
- md5 train-val = 0, train-test = 0, val-test = 0.

**Bảng 14:** Phân bố số ảnh theo split, domain và lớp sau khi chia stratified

| split | domain | label | n_images |
|-------|--------|-------|----------|
| test | coffee | LeafMiner | 180 |
| test | coffee | Rust | 208 |
| test | coffee | AlgalLeafSpot | 143 |
| test | coffee | PowderyMildew | 39 |
| test | rice | BrownSpot | 79 |
| test | rice | Healthy | 221 |
| test | rice | Hispa | 86 |
| test | rice | LeafBlast | 117 |
| train | coffee | LeafMiner | 840 |
| train | coffee | Rust | 971 |
| train | coffee | AlgalLeafSpot | 664 |
| train | coffee | PowderyMildew | 183 |
| train | rice | BrownSpot | 372 |
| train | rice | Healthy | 1030 |
| train | rice | Hispa | 400 |
| train | rice | LeafBlast | 544 |
| val | coffee | LeafMiner | 180 |
| val | coffee | Rust | 208 |
| val | coffee | AlgalLeafSpot | 142 |
| val | coffee | PowderyMildew | 40 |
| val | rice | BrownSpot | 80 |
| val | rice | Healthy | 221 |
| val | rice | Hispa | 85 |
| val | rice | LeafBlast | 116 |

**Bảng 15:** Tỉ lệ split toàn cục sau chia dữ liệu

| split | ratio (%) |
|-------|-----------|
| train | 70.00 |
| val | 15.00 |
| test | 15.01 |

**Nhận xét:** Việc không có giao cắt giữa các split theo cả sample_id lẫn MD5 cho thấy leakage được kiểm soát ở mức nội dung chứ không chỉ ở mức tên tệp. Đồng thời, tỉ lệ split bám sát mục tiêu 70/15/15 và phân bố lớp giữa validation–test tương đối ổn định, nên sai khác hiệu năng giữa hai tập này về sau sẽ chủ yếu phản ánh hành vi mô hình thay vì sai lệch do sampling.

### 4.4 Chuẩn hóa ảnh và lưu vào data/processed/images

Sau khi chia tập, mọi ảnh được chuẩn hóa về canvas vuông 256×256 bằng resize theo cạnh dài rồi padding đối xứng. Việc xuất trước bộ ảnh đã chuẩn hóa giúp khóa chặt đầu vào của các thí nghiệm, giảm khác biệt do tiền xử lý được chạy lại ở những thời điểm khác nhau.

**Định nghĩa 4.4** (Chuẩn hóa hình học bằng resize và padding đối xứng). Cho ảnh có kích thước gốc $(W, H)$ và canvas chuẩn hóa kích thước $S = \text{canvas\_size}$. Hệ số co giãn theo cạnh dài được xác định bởi

$$\text{scale} = \frac{S}{\max(W, H)} \tag{4.7}$$

Kích thước sau resize là

$$W' = \lfloor W \cdot \text{scale} \rceil, \quad H' = \lfloor H \cdot \text{scale} \rceil \tag{4.8}$$

và tổng phần bù đệm để đưa về ảnh vuông là

$$\text{pad\_w} = S - W', \quad \text{pad\_h} = S - H' \tag{4.9}$$

Padding được phân bổ đối xứng theo hai phía:

$$p_{left} = \left\lfloor \frac{\text{pad\_w}}{2} \right\rfloor, \quad p_{right} = \text{pad\_w} - p_{left}, \quad p_{top} = \left\lfloor \frac{\text{pad\_h}}{2} \right\rfloor, \quad p_{bottom} = \text{pad\_h} - p_{top} \tag{4.10}$$

**Lý do lựa chọn và đánh đổi:** Resize kèm padding được ưu tiên hơn resize trực tiếp về ảnh vuông vì hình thái tổn thương — chẳng hạn đốm nhỏ, vệt cháy dài hoặc biên tổn thương méo — mang giá trị chẩn đoán trực tiếp. Phép warp trực tiếp có thể làm thay đổi chính tín hiệu mà mô hình cần học. Một alternative là resize cứng về kích thước chuẩn; cách này đơn giản và tận dụng toàn bộ diện tích canvas, nhưng trả giá bằng méo hình. Alternative khác là crop bám theo lá hoặc vùng bệnh; cách đó có thể tăng mật độ tín hiệu hữu ích, nhưng đòi hỏi bước phân đoạn hoặc heuristic cắt ảnh ổn định, đồng thời làm tăng nguy cơ mất tổn thương nhỏ gần biên. Đánh đổi của padding là tạo thêm vùng nền không thông tin và làm giảm diện tích nội dung thực trên canvas; tuy nhiên, với dữ liệu có tỉ lệ khung hình đa dạng như ở đây, đánh đổi này hợp lý hơn so với việc để mô hình học méo hình như một shortcut theo domain. Nội suy BICUBIC được giữ lại vì nó cho kết quả thu nhỏ ổn định và ít răng cưa hơn các phép nội suy đơn giản, dù có thể làm mềm nhẹ một số biên rất sắc.

Kết quả xuất ảnh chuẩn hóa giữ nguyên phân bố số lượng theo split/lớp như Bảng 14, với tổng số ảnh đã xuất là 7149.

**Nhận xét:** Bước chuẩn hóa hình học ở đây không chỉ nhằm đưa ảnh về cùng kích thước đầu vào, mà còn nhằm kiểm soát một nguồn lệch miền quan trọng: khác biệt hình học giữa hai domain. Việc giữ tỉ lệ trước khi resize giúp giảm khả năng mô hình tận dụng biến dạng hình học như một tín hiệu phụ để nhận biết domain thay vì bệnh.

### 4.5 Tính thống kê chuẩn hóa (mean/std) trên train split

Thống kê chuẩn hóa chỉ được tính trên train split để tránh leakage, sau đó lưu vào tệp cấu hình dùng chung cho các bước train/eval.

**Định nghĩa 4.5** (Chuẩn hóa theo kênh trên train split). Với mỗi kênh màu $c \in \{R, G, B\}$, công thức chuẩn hóa pixel được xác định bởi

$$\hat{x}_c = \frac{x_c/255 - \mu_c}{\sigma_c} \tag{4.11}$$

trong đó trung bình và độ lệch chuẩn của kênh $c$ được tính theo dạng online trên toàn bộ pixel của train split:

$$\mu_c = \frac{\sum_{i,x,y} I_c(i,x,y)}{N_{total\_pixels}} \tag{4.12}$$

$$\sigma_c = \sqrt{\frac{\sum_{i,x,y} I_c^2(i,x,y)}{N_{total\_pixels}} - \mu_c^2} \tag{4.13}$$

**Lý do lựa chọn và đánh đổi:** Chuẩn hóa theo thống kê của chính train split được chọn thay vì dùng trực tiếp mean/std chuẩn của ImageNet. Lựa chọn dùng thống kê sẵn có từ pretraining là một alternative hợp lý khi mục tiêu là đồng bộ tuyệt đối với backbone tiền huấn luyện; tuy nhiên, trong bộ dữ liệu này, EDA đã cho thấy khác biệt quang học đáng kể giữa hai domain và giữa các lớp. Vì vậy, thống kê riêng của train split phản ánh dữ liệu thực tế tốt hơn và giúp giảm chênh lệch thang đo giữa các kênh đầu vào. Đánh đổi là mức độ "chuẩn hóa theo chuẩn công nghiệp" giảm đi đôi chút, nhưng lợi ích về tính nhất quán với phân phối dữ liệu huấn luyện lớn hơn. Việc tính theo dạng online cũng là lựa chọn thực dụng: nó giữ chi phí bộ nhớ thấp mà vẫn cho thống kê chính xác trên 5004 ảnh train.

**Bảng 16:** Thống kê normalization tính trên train split

| Thuộc tính | Giá trị |
|------------|---------|
| source | train_split_only |
| num_images | 5004 |
| mean (R, G, B) | (0.546091, 0.571719, 0.541244) |
| std (R, G, B) | (0.322439, 0.315874, 0.357553) |

**Nhận xét:** Độ lệch chuẩn giữa các kênh không hoàn toàn đồng nhất, đặc biệt kênh B có mức phân tán lớn nhất. Insight này phù hợp với quan sát EDA rằng nhiễu quang học của dữ liệu không thuần nhất; do đó, normalization không chỉ là bước chuẩn hóa số học, mà còn là cơ chế làm suy yếu các biến thiên màu sắc ngoại sinh trước khi mô hình học đặc trưng bệnh.

### 4.6 Thiết lập augmentation cho train/val/test

Augmentation được thiết kế theo nguyên tắc: tăng tính bất biến với các biến thiên có thể xảy ra ngoài thực địa, nhưng không phá hủy các dấu hiệu hình thái vốn mang giá trị chẩn đoán. Vì vậy, pipeline tách rõ train transform (ngẫu nhiên) và eval transform (xác định).

Về nhóm biến đổi hình học, các phép crop/flip/affine mô phỏng thay đổi góc nhìn, khoảng cách và định hướng lá trong điều kiện chụp thực tế. Về nhóm biến đổi quang học, ColorJitter được dùng để làm mô hình bền vững hơn trước khác biệt về ánh sáng tự nhiên, thay vì áp đặt một quy trình hiệu chỉnh màu cứng nhắc ngay ở giai đoạn tiền xử lý. RandomErasing đóng vai trò regularization cho các trường hợp che khuất cục bộ hoặc nền nhiễu.

**Định nghĩa 4.6** (MixUp và CutMix). Với MixUp, hai mẫu $(x_i, y_i)$ và $(x_j, y_j)$ được trộn theo $\lambda \sim \text{Beta}(\alpha, \alpha)$:

$$\tilde{x} = \lambda x_i + (1 - \lambda) x_j, \quad \tilde{y} = \lambda y_i + (1 - \lambda) y_j \tag{4.14}$$

Với CutMix, dữ liệu đầu vào được trộn theo mặt nạ không gian nhị phân $M$:

$$\tilde{x} = M \odot x_i + (1 - M) \odot x_j \tag{4.15}$$

và nhãn được hiệu chỉnh theo tỉ lệ diện tích vùng cắt dán:

$$\tilde{y} = \lambda_{adj} y_i + (1 - \lambda_{adj}) y_j, \quad \lambda_{adj} = 1 - \frac{(x_2 - x_1)(y_2 - y_1)}{W \cdot H} \tag{4.16}$$

Trong cả hai trường hợp, nhãn mới là tổ hợp lồi của hai nhãn gốc, nên phù hợp với thiết lập huấn luyện bằng soft labels.

**Lý do lựa chọn và đánh đổi:** Thiết kế augmentation được giữ ở mức vừa phải thay vì đẩy mạnh tối đa. RandomResizedCrop dùng dải scale 0.75–1.0 để tăng đa dạng bố cục nhưng vẫn hạn chế nguy cơ cắt mất tổn thương nhỏ; crop mạnh hơn là alternative có thể tăng regularization, nhưng không phù hợp khi vùng bệnh nhiều khi chỉ chiếm tỉ lệ nhỏ của ảnh. HorizontalFlip và VerticalFlip phản ánh sự đa dạng định hướng khi chụp ngoài thực địa, song xác suất lật dọc được đặt thấp hơn để tránh tạo quá nhiều mẫu ít tự nhiên. RandomAffine và ColorJitter được chọn nhằm mô phỏng đúng hai nguồn biến thiên chính đã chỉ ra trong EDA là góc chụp và chiếu sáng; các alternative như histogram equalization, CLAHE hay color constancy có thể chuẩn hóa ảnh mạnh hơn, nhưng cũng dễ can thiệp quá mức vào tín hiệu màu của bệnh. RandomErasing hữu ích để giảm phụ thuộc vào một vùng cục bộ duy nhất, nhưng nếu dùng quá mạnh có thể xóa luôn dấu hiệu bệnh. Với MixUp, lợi ích chính là làm mượt biên quyết định và giảm hiện tượng overconfidence; trade-off là hình thái cục bộ của tổn thương bị làm mềm. CutMix khắc phục phần nào điểm này bằng cách giữ lại texture cục bộ tốt hơn, nhưng đổi lại sinh ra các ảnh ghép kém tự nhiên hơn. Vì không có một kỹ thuật đơn lẻ nào bao phủ tốt mọi loại nhiễu, pipeline sử dụng tổ hợp augmentation ở cường độ trung bình để cân bằng giữa độ đa dạng nhân tạo và độ trung thực sinh học của triệu chứng.

**Các cấu hình quan trọng được in ra từ output:**

- Train transform: RandomResizedCrop(224), HorizontalFlip(p=0.5), VerticalFlip(p=0.2), RandomAffine(±30°), ColorJitter, RandomErasing(p=0.5), Normalize.
- Eval transform: CenterCrop(224), ToTensor, Normalize.

**Nhận xét:** Điểm mạnh của thiết kế augmentation hiện tại là tính điều độ. Mục tiêu không phải tạo ra một phân phối nhân tạo thật rộng, mà là mở rộng vừa đủ quanh phân phối thực địa để mô hình bền vững hơn mà không đánh mất ý nghĩa sinh học của triệu chứng. Việc dùng CenterCrop cho đánh giá cũng giữ cho phép đo ổn định và nhất quán với pipeline huấn luyện, thay vì đưa thêm ngẫu nhiên không cần thiết vào pha validation/test.

**Bảng 17:** Lý do chọn kỹ thuật augmentation và tham số chính

| Kỹ thuật | Lý do chọn | Tham số chính |
|----------|------------|---------------|
| RandomResizedCrop | Tăng đa dạng bố cục nhưng giữ crop ở mức bảo thủ để tránh mất tổn thương nhỏ | scale 0.75–1.0 |
| HorizontalFlip | Khai thác sự thay đổi hướng chụp trái/phải của lá ngoài thực địa | p = 0.5 |
| VerticalFlip | Bao quát thêm biến thiên định hướng nhưng dùng xác suất thấp để giữ tính tự nhiên | p = 0.2 |
| RandomAffine | Mô phỏng xoay/dịch nhẹ do góc cầm máy và phối cảnh thực tế | ±30° |
| ColorJitter | Tăng bền vững trước thay đổi điều kiện ánh sáng và màu sắc môi trường | b = 0.3, c = 0.3 |
| RandomErasing | Hạn chế phụ thuộc vào một vùng cục bộ, tăng regularization | p = 0.5, scale 0.02–0.15 |
| MixUp | Làm mượt biên quyết định bằng soft labels | α = 0.4 |
| CutMix | Giữ được đặc trưng cục bộ tốt hơn khi trộn mẫu | α = 1.0 |

### 4.7 Cân bằng lớp cho train loader và lưu cấu hình tiền xử lý

Mất cân bằng lớp trong train split được xử lý ở mức dữ liệu bằng WeightedRandomSampler với trọng số nghịch đảo tần suất lớp.

**Định nghĩa 4.7** (Lấy mẫu nghịch đảo tần suất lớp). Với lớp $c$ trong train split, trọng số lấy mẫu được xác định bởi

$$w_c = \frac{1}{|D^c_{train}|} \tag{4.17}$$

và xác suất lấy mẫu thứ $i$ có nhãn $y_i$ tỷ lệ theo trọng số lớp

$$P(i) = \frac{w_{y_i}}{\sum_j w_{y_j}} \tag{4.18}$$

**Lý do lựa chọn và đánh đổi:** Quyết định ưu tiên WeightedRandomSampler thay vì chỉ dùng class-weighted loss xuất phát từ nhu cầu cân bằng tần suất xuất hiện của lớp hiếm trong từng mini-batch. Nếu chỉ tăng trọng số trong hàm mất mát, mô hình vẫn có thể nhìn thấy lớp thiểu số quá ít lần trong một epoch, đặc biệt khi số mẫu ít như PowderyMildew. Ngược lại, weighted sampling làm tăng số lần mô hình tiếp xúc với các lớp hiếm dưới nhiều biến thể augmentation khác nhau, tức giải quyết lệch lớp ở ngay đầu vào của quá trình tối ưu. Alternative gồm class-weighted cross-entropy hoặc focal loss; các lựa chọn này hữu ích khi muốn điều chỉnh gradient mà không lặp lại mẫu, nhưng chúng không trực tiếp sửa mất cân bằng thành phần mini-batch. Đánh đổi của weighted sampling là hiện tượng lặp lại ảnh hiếm và khả năng khuếch đại nhiễu nhãn nếu dữ liệu bẩn. Trong bối cảnh hiện tại, sau bước làm sạch và kiểm soát trùng lặp, đánh đổi này chấp nhận được. Để tránh over-correction, cấu hình cơ sở chưa kết hợp đồng thời sampler với class-weighted loss.

Khi sử dụng `replacement=True`, lớp thiểu số được oversampling thông qua cơ chế lấy lặp để cân bằng tần suất xuất hiện theo mini-batch.

Ngoài ra, quy trình xác nhận đã lưu đầy đủ manifest tiền xử lý. Tệp cấu hình đi kèm là `preprocessing_config.json` và chiều dài sampler được cố định ở 5004 mẫu.

**Nhận xét:** Trọng số lấy mẫu cho thấy lớp PowderyMildew nhận mức ưu tiên cao nhất, phù hợp với mức mất cân bằng đã quan sát ở EDA. Điểm đáng lưu ý là bước cân bằng này làm cho mục tiêu huấn luyện nhất quán hơn với thước đo Macro-F1 ở giai đoạn đánh giá: mô hình không chỉ được thưởng vì dự đoán tốt lớp phổ biến, mà còn buộc phải học nghiêm túc các lớp hiếm.

**Bảng 18:** Thống kê class count và sampling weight trong train split

| label | class_count | sampling_weight |
|-------|-------------|-----------------|
| LeafMiner | 840 | 0.001190 |
| BrownSpot | 372 | 0.002688 |
| Rust | 971 | 0.001030 |
| AlgalLeafSpot | 664 | 0.001506 |
| Healthy | 1030 | 0.000971 |
| Hispa | 400 | 0.002500 |
| LeafBlast | 544 | 0.001838 |
| PowderyMildew | 183 | 0.005464 |

### 4.8 Kết luận và đầu ra của giai đoạn tiền xử lý

Tổng thể, pipeline tiền xử lý hoàn thành đầy đủ các khâu chính: hợp nhất metadata, làm sạch dữ liệu, chia tập chống leakage, chuẩn hóa hình học, tính thống kê normalization trên train, thiết kế augmentation, cân bằng lớp bằng weighted sampling và lưu cấu hình phục vụ huấn luyện/đánh giá.

**Các đầu ra chính gồm:**

- bộ ảnh đã chuẩn hóa theo split trong `data/processed/images`;
- manifest chống leakage cho train/val/test trong `data/processed/metadata`;
- tệp `normalization_stats.json` và tệp cấu hình tổng quát `preprocessing_config.json`.

**Bảng 19:** Tóm tắt đầu ra định lượng quan trọng của giai đoạn preprocessing

| Hạng mục | Kết quả |
|----------|---------|
| Tổng ảnh ban đầu | 7300 |
| Tổng ảnh sau làm sạch | 7149 |
| Ngưỡng lọc blur toàn cục | 8.3284 (quantile 2%) |
| Tỉ lệ chia dữ liệu | train 70.00%, val 15.00%, test 15.01% |
| Số ảnh train để tính mean/std | 5004 |
| Kích thước ảnh chuẩn hóa | 256×256 (padding giữ tỉ lệ) |
| Chuẩn hóa cho mô hình | crop 224×224 + normalize theo train stats |

**Nhận xét:** Giá trị cốt lõi của giai đoạn preprocessing không nằm ở việc làm dữ liệu "đẹp" hơn, mà ở chỗ biến dữ liệu thô, không đồng nhất và dễ rò rỉ thành một đầu vào có thể huấn luyện, so sánh và tái lập một cách công bằng. Vì vậy, những kết quả ở giai đoạn mô hình phía sau có thể được quy chủ yếu cho lựa chọn kiến trúc và chiến lược học, thay vì cho các sai lệch ẩn trong pipeline tiền xử lý.

---

## Tài liệu tham khảo

[1] Google DeepMind. Gemma 4. https://deepmind.google/models/gemma/gemma-4/, April 2026.

[2] ggml-org. llama.cpp. https://github.com/ggml-org/llama.cpp, 2026. GitHub repository: LLM inference in C/C++. Accessed: May 2, 2026.

[3] Daniel Han, Michael Han, and Unsloth team. Unsloth. https://github.com/unslothai/unsloth, 2023. GitHub repository. Accessed: May 2, 2026.
