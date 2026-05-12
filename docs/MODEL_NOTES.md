# Model Notes — Baseline models & Advanced models

### Cấu trúc models

Nhìn vào 5 model được phân công:

| Model | Người phụ trách | Vai trò thực tế |
|---|---|---|
| **U-Net** | Tuấn Anh | **Baseline semantic segmentation model** |
| **YOLOv8-seg** | Tống Phúc | **Baseline instance segmentation model** |
| RF-DETR | Anh Tuấn | Advanced model |
| Mask R-CNN | Xuân Trí | Advanced model |
| Mask2Former | Đàm Đạt | SOTA model |

---

### Lưu ý khi viết báo cáo

Khi trình bày kết quả, cần **frame U-Net và YOLOv8-seg như baseline** một cách rõ ràng:

```
U-Net (Baseline):  mIoU = X%, Dice = Y%
YOLOv8-seg (Baseline):  mIoU = X+δ%, Dice = Y+δ%
Mask R-CNN:        ...
Mask2Former:       ...
RF-DETR:           ...
```
