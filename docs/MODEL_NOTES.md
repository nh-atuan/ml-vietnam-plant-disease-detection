# Model Notes — Baseline models & Advanced models

### Cấu trúc models

Nhìn vào 5 model được phân công:

| Model | Người phụ trách | Vai trò thực tế | Resources |
| :--- | :--- | :--- | :--- |
| **Mask R-CNN** | Xuân Trí | CNN-based model (Baseline) | [MaskRCNN Resnet50](https://github.com/magnusdtd/AIC-HCMUS-Fragment-Segmentation/blob/main/notebook/gdgoc-hcmus-aic-maskrcnn-resnet50-fpn.ipynb) |
| **YOLO26-seg** | Anh Tuấn | CNN-based model | [Fine-tune YOLO26-seg](https://colab.research.google.com/drive/1tYi19epfw6jUgaIUD03cgsGMC-NXI6KB?usp=sharing) |
| **RT-DETR** | Tống Phúc| Vision Transformer-based model (SOTA) | [RF-DETR Roboflow Train Guide](https://rfdetr.roboflow.com/learn/train/) |
| **MobileSAM** | Đàm Đạt | Vision Transformer-based model | [MobileSAM Fast Finetuning](https://github.com/KdaiP/MobileSAM-fast-finetuning) |
| **Mask2Former** | Tuấn Anh | Vision Transformer-based model | [Fine-tuning Mask2Former](https://debuggercafe.com/fine-tuning-mask2former/) |

---

### Lưu ý 
- Set seed ở đầu notebook
- Push weight lên một Hugging Face repo
- Sử dụng các phương pháp augmentation đã nêu trong báo cáo/proposal.
