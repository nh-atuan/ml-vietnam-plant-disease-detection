# Model Notes — Ghi chú Kỹ thuật & Phương pháp luận

---

## Có cần chọn Baseline Model không?

**Ngắn gọn: Có, nhưng trong dự án này U-Net _đã là_ baseline rồi — không cần train riêng một bước trước.**

---

### Tại sao cần baseline?

Trong nghiên cứu ML, baseline model phục vụ hai mục đích:
1. **Điểm tham chiếu** — để biết các model phức tạp hơn có thực sự cải thiện hay không
2. **Kiểm tra sanity** — nếu model "xịn" mà thua baseline thì có gì đó sai

---

### Cấu trúc hiện tại của nhóm ĐÃ đủ baseline

Nhìn vào 5 model được phân công:

| Model | Người phụ trách | Vai trò thực tế |
|---|---|---|
| **U-Net** | Đàm Đạt | ✅ **Baseline** — kiến trúc cổ điển, đơn giản, well-understood |
| YOLOv8-seg | Xuân Trí | Advanced (real-time) |
| Mask R-CNN | Tống Phúc | Advanced (instance seg) |
| Mask2Former | Tuấn Anh | SOTA (transformer-based) |
| RF-DETR | Anh Tuấn | Advanced (detection + seg) |

> U-Net là lựa chọn baseline chuẩn mực cho bài toán segmentation — gần như mọi paper segmentation đều so sánh với U-Net.

---

### Không cần train theo thứ tự "baseline trước"

Vì mỗi người train **độc lập trên Kaggle notebook riêng**, nhóm có thể:
- Train **song song** tất cả 5 model cùng lúc
- Sau đó **tổng hợp metrics** vào bảng so sánh cuối Phase 3+4

Không có lý do kỹ thuật nào bắt buộc phải train U-Net xong mới train cái khác.

---

### Lưu ý khi viết báo cáo

Khi trình bày kết quả, cần **frame U-Net như baseline** một cách rõ ràng:

```
U-Net (Baseline):  mIoU = X%, Dice = Y%
YOLOv8-seg:        mIoU = X+δ%, Dice = Y+δ%  (+Z% so với baseline)
Mask R-CNN:        ...
Mask2Former:       ...
RF-DETR:           ...
```

Điều này cho thấy nhóm hiểu phương pháp luận nghiên cứu — tăng điểm học thuật.

---

### Kết luận

Không cần thay đổi gì trong `PLAN.md`. Chỉ cần đảm bảo trong báo cáo cuối, U-Net được gọi rõ là **"baseline model"** và các model khác được so sánh delta so với nó.
