# KẾ HOẠCH PHÂN CÔNG ĐỒ ÁN CUỐI KỲ - MODEL PHASE
## Hệ thống chẩn đoán bệnh trên lá cây nông nghiệp (Cà phê / Lúa)

---

## Thông tin nhóm

| STT | Họ và tên | MSSV |
|-----|-----------|------|
| 1 | Lê Xuân Trí | 23120099 |
| 2 | Đàm Tiến Đạt | 23120118 |
| 3 | Tống Thanh Phúc | 23120158 |
| 4 | Dương Tuấn Anh | 23120208 |
| 5 | Nguyễn Hồ Anh Tuấn | 23120185 |

> **Giảng viên hướng dẫn:** Thầy Bùi Tiến Lên

---

## Tổng quan mốc thời gian (Model Phase)

| Mốc | Thời điểm | Phase | Nội dung yêu cầu nộp | Trạng thái |
|-----|-----------|-------|----------------------|------------|
| Tuần 7–9 | Training | 3+4 | **Lựa chọn, Huấn luyện, Đánh giá & Tinh chỉnh** – 5 model segmentation trên Kaggle GPU, push HuggingFace Hub, báo cáo tiến độ lần 2 (dự kiến 24/5) | Đang thực hiện |

---

## PHASE 3 — Lựa chọn, Huấn luyện & Đánh giá Mô hình (Segmentation)
> **Tuần 7 → Tuần 9** | **Deadline: 31/5**

### Mục tiêu Phase 3
- Mỗi thành viên chọn **1 mô hình segmentation**, tự huấn luyện và đánh giá trên **Kaggle Notebook** (GPU T4/P100, 30h/tuần)
- **Mỗi model được train & evaluate trên 2 notebook riêng biệt** — 1 cho tập lúa (Rice), 1 cho tập cà phê (Coffee) — giúp tách biệt phân phối dữ liệu, dễ debug và chạy song song
- Kết quả evaluation từ cả 5 model sẽ được tổng hợp để **chọn ra best model** cho Phase 4 (tuning)
- Train xong → **push model lên HuggingFace Hub** để nhóm dùng chung qua API
- Commit notebook đã chạy lên repo tại `notebooks/models/<tên_model>/`
- Bài toán: **Instance/Semantic Segmentation** — từ ảnh lá cây xác định vùng bệnh + nhãn bệnh
- Áp dụng Data Augmentation (Affine, Intensity Transformation, CutMix, CutOut, Mixup) để tăng cường dữ liệu và chống overfitting

> **Lý do không dùng MLflow / train local:** PyTorch segmentation models cần GPU; train trên CPU mất hàng chục giờ/epoch. Kaggle cung cấp GPU miễn phí 30h/tuần — đủ để train và tune. MLflow được thay bằng HuggingFace Hub để lưu & serve model.

> **Lý do tách 2 notebook theo dataset:** Lúa và cà phê có đặc điểm hình thái lá, màu sắc và phân phối bệnh khác nhau rõ rệt. Tách notebook giúp mỗi thành viên chạy độc lập trên Kaggle (tránh conflict GPU quota), kết quả per-dataset rõ ràng và dễ so sánh cross-dataset.

### 5 Mô hình Segmentation được chọn

| Model | Đặc điểm | Tham khảo |
|-------|----------|----------|
| **Mask R-CNN** | CNN-based model (Baseline) | [MaskRCNN Resnet50](https://github.com/magnusdtd/AIC-HCMUS-Fragment-Segmentation/blob/main/notebook/gdgoc-hcmus-aic-maskrcnn-resnet50-fpn.ipynb) |
| **YOLO26-seg** | CNN-based model | [Fine-tune YOLO26-seg](https://colab.research.google.com/drive/1tYi19epfw6jUgaIUD03cgsGMC-NXI6KB?usp=sharing) |
| **RF-DETR** | Vision Transformer-based model (SOTA) | [RF-DETR Roboflow Train Guide](https://rfdetr.roboflow.com/learn/train/) |
| **MobileSAM** | Vision Transformer-based model | [MobileSAM Fast Finetuning](https://github.com/KdaiP/MobileSAM-fast-finetuning) |
| **Mask2Former** | Vision Transformer-based model | [Fine-tuning Mask2Former](https://debuggercafe.com/fine-tuning-mask2former/) |

### Phân công công việc

| # | Mô hình | Người phụ trách | Output |
|---|---------|-----------------|--------|
| 3.1 | **Mask R-CNN**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Xuân Trí** | Commit notebook vào `notebooks/models/mask_rcnn/` + push model lên HuggingFace |
| 3.2 | **YOLO26-seg**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Anh Tuấn** | Commit notebook vào `notebooks/models/yolo26_seg/` + push model lên HuggingFace |
| 3.3 | **RF-DETR**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Tống Phúc** | Commit notebook vào `notebooks/models/rf_detr/` + push model lên HuggingFace |
| 3.4 | **MobileSAM**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Đàm Đạt** | Commit notebook vào `notebooks/models/mobilesam/` + push model lên HuggingFace |
| 3.5 | **Mask2Former**: train + evaluate trên Kaggle (2 notebook: Rice & Coffee) | **Tuấn Anh** | Commit notebook vào `notebooks/models/mask2former/` + push model lên HuggingFace |
| 3.6 | Tổng hợp kết quả evaluation, lập bảng so sánh đa tiêu chí, **chọn best model** chuyển sang Phase 4 | **Đàm Đạt** | Bảng so sánh đa tiêu chí + quyết định best model (ghi vào README) |
| 3.7 | Viết báo cáo tiến độ lần 2 — phần **Benchmark & Evaluation** (tổng quan 5 model, bảng kết quả, phân tích lựa chọn best model) | **Tống Phúc** | Phần Benchmark trong báo cáo tiến độ lần 2 |
| 3.8 | Hỗ trợ viết báo cáo benchmark: bổ sung phân tích so sánh định tính giữa các kiến trúc CNN và Transformer, nhận xét về trade-off accuracy vs. inference time | **Tuấn Anh** | Bổ sung phân tích kiến trúc trong phần Benchmark |
| 3.9 | Hỗ trợ viết báo cáo benchmark: vẽ biểu đồ so sánh (bar chart mAP, mIoU, inference time), bảng heat-map per-class performance, nhận xét trực quan | **Xuân Trí** | Biểu đồ + bảng so sánh hình ảnh trong phần Benchmark |

### Quy trình mỗi thành viên cần thực hiện

```
[Notebook 1 — Rice dataset]
1. Tạo Kaggle Notebook → kết nối dataset Rice (lọc từ data/processed/ theo plant_type)
2. Implement pipeline: load data → augmentation → train → validate
3. Evaluate: mAP@50, mAP@50:95, mIoU, Dice Score, inference time
4. Lưu best checkpoint Rice → push lên HuggingFace Hub

[Notebook 2 — Coffee dataset]
5. Lặp lại bước 1–4 cho tập cà phê
6. Ghi nhận kết quả cả 2 tập → report vào bảng so sánh nhóm
7. Download notebook đã chạy (có output) → commit vào repo
```

### Thiết lập huấn luyện chung

| Hạng mục | Chi tiết |
|----------|----------|
| **Môi trường** | Kaggle Notebook (GPU T4 x2 hoặc P100) |
| **Dataset** | Upload `data/processed/` lên Kaggle Dataset; lọc theo `plant_type` (rice / coffee) trong notebook |
| **Metrics chính** | mAP@50, mAP@50:95, mIoU, Dice Score |
| **Model hosting** | HuggingFace Hub (public repo của nhóm) |
| **Commit vào repo** | Notebook `.ipynb` đã có output đầy đủ |

### Cấu trúc thư mục

```
notebooks/
  models/
    mask_rcnn/
      train_eval_rice.ipynb       ← Kaggle notebook Rice đã chạy
      train_eval_coffee.ipynb     ← Kaggle notebook Coffee đã chạy
      README.md                   ← mô tả kết quả, link HuggingFace
    yolo26_seg/
      train_eval_rice.ipynb
      train_eval_coffee.ipynb
      README.md
    rf_detr/
    mobilesam/
    mask2former/
```

### Kết quả cần đạt cuối Phase 3

> **Output/Artifacts sau khi huấn luyện 5 mô hình:** [Google Drive — Training Outputs](https://drive.google.com/drive/folders/1L5tih3t2_aAUrNUAEsf5aejOtmnY2oFR?usp=sharing) *(checkpoints, logs, metrics, biểu đồ — phục vụ benchmark & viết báo cáo)*

| Hạng mục | Mô tả |
|----------|-------|
| 10 notebooks | Mỗi model 2 notebook Kaggle (Rice + Coffee) đã chạy đầy đủ (train + eval) |
| 10 model checkpoints trên HuggingFace | Best checkpoint per-dataset của mỗi model push lên HF Hub |
| Bảng so sánh | mAP@50, mIoU, inference time, model size — per model, per dataset |
| **Best model được chọn** | 1 model (+ dataset) được chọn để chuyển sang Phase 4 tuning |
| Báo cáo tiến độ 2 | Phần Model + Evaluation hoàn chỉnh |

---

## PHASE 4 — Tinh chỉnh Mô hình Tốt Nhất (Hyperparameter Tuning)
> **Sau khi Phase 3 hoàn thành & best model được chọn** | **Deadline: 7/6**

### Mục tiêu Phase 4
- Chỉ tune **1 model duy nhất** — model được chọn từ bảng so sánh Phase 3
- Sử dụng **RayTune + ASHA (Asynchronous Successive Halving Algorithm)** để tối ưu hyperparameter hiệu quả: early-stop các trial kém ngay từ đầu, tập trung tài nguyên GPU vào các config hứa hẹn
- Kết quả tuning sẽ là checkpoint cuối cùng để export ONNX và deploy

> **Lý do tách tuning ra khỏi Phase 3:** Tuning tất cả 5 model song song là lãng phí GPU quota. Chỉ tune model đã được chứng minh tốt nhất qua evaluation → tối ưu tài nguyên và thời gian.

> **Lý do dùng ASHA thay vì grid/random search:** ASHA tự động loại bỏ sớm các trial kém hiệu năng (early stopping dựa trên intermediate results), cho phép thử nhiều config hơn trong cùng thời gian GPU, đặc biệt phù hợp với giới hạn 30h/tuần của Kaggle.

### Không gian tìm kiếm Hyperparameter (Search Space)

| Hyperparameter | Search Space gợi ý |
|----------------|-------------------|
| **Learning Rate** | `loguniform(1e-5, 1e-2)` |
| **Batch Size** | `choice([4, 8, 16])` |
| **Epochs** | `choice([20, 30, 50])` |
| **Backbone / Neck** | `choice([...])` (tùy model) |
| **Augmentation level** | `choice(['light', 'medium', 'heavy'])` |
| **Weight Decay** | `loguniform(1e-5, 1e-2)` |

### Cấu hình ASHA Scheduler

```python
from ray import tune
from ray.tune.schedulers import ASHAScheduler

scheduler = ASHAScheduler(
    metric="mAP50",          # metric để đánh giá trial
    mode="max",
    max_t=50,                # số epoch tối đa mỗi trial
    grace_period=5,          # số epoch tối thiểu trước khi có thể prune
    reduction_factor=3,      # mỗi lần halving, giữ lại 1/3 trials tốt nhất
)

tuner = tune.Tuner(
    train_fn,
    param_space=search_space,
    tune_config=tune.TuneConfig(
        scheduler=scheduler,
        num_samples=20,      # tổng số config thử
    ),
)
results = tuner.fit()
```

### Quy trình Phase 4

```
1. Xác nhận best model từ bảng so sánh Phase 3 (cả nhóm quyết định)
2. Tạo Kaggle Notebook mới: tune_<model_name>_<dataset>.ipynb
3. Cài đặt ray[tune] (pip install "ray[tune]")
4. Định nghĩa search space và ASHA scheduler
5. Chạy tuning (num_samples ≥ 15 trials)
6. Lấy best config → train lại với best config trên full train set
7. Evaluate lần cuối trên test set → so sánh với baseline Phase 3
8. Export checkpoint tốt nhất → push lên HuggingFace Hub (override best checkpoint)
9. Commit notebook đã chạy vào repo
```

### Phân công công việc

| # | Công việc | Người phụ trách | Output |
|---|-----------|-----------------|--------|
| 4.1 | Xác nhận best model từ bảng so sánh Phase 3, thống nhất toàn nhóm | **Đàm Đạt** | Biên bản chọn model (ghi vào README) |
| 4.2 | Setup RayTune + ASHA, implement tuning notebook cho best model | **Đàm Đạt** | `notebooks/models/<model>/tune_<dataset>.ipynb` |
| 4.3 | Retrain với best config, evaluate cuối, push checkpoint lên HuggingFace | **Đàm Đạt** | Checkpoint final trên HuggingFace Hub |
| 4.4 | Viết báo cáo phần **Tuning**: bảng before/after metrics, phân tích hyperparameter sensitivity, kết luận | **Anh Tuấn** | Phần Tuning trong báo cáo tiến độ 2 |
| 4.5 | Hỗ trợ viết báo cáo tuning: trình bày lý thuyết ASHA scheduler, giải thích search space, liên hệ với kết quả Phase 3 | **Tuấn Anh** | Lý thuyết & phân tích ASHA trong phần Tuning |
| 4.6 | Hỗ trợ viết báo cáo tuning: vẽ biểu đồ learning curve before/after tuning, loss surface visualization, trial performance chart của RayTune | **Xuân Trí** | Biểu đồ minh họa trong phần Tuning |

### Tiêu chí chọn mô hình tốt nhất (từ Phase 3)

1. **mAP@50:95** — độ chính xác segmentation tổng thể
2. **mIoU** — chất lượng phân vùng
3. **Inference time** — phù hợp web serving (mục tiêu < 500ms/ảnh trên CPU)
4. **Model size** — khả năng deploy
5. **Độ ổn định** — train/val gap hợp lý

### Bảng so sánh mô hình Phase 3 (template — điền sau khi train xong)

| Mô hình | Dataset | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) | Size (MB) |
|---------|---------|--------|-----------|------|------|----------------|-----------|
| Mask R-CNN | Rice | — | — | — | — | — | — |
| Mask R-CNN | Coffee | — | — | — | — | — | — |
| YOLO26-seg | Rice | — | — | — | — | — | — |
| YOLO26-seg | Coffee | — | — | — | — | — | — |
| RF-DETR | Rice | — | — | — | — | — | — |
| RF-DETR | Coffee | — | — | — | — | — | — |
| MobileSAM | Rice | — | — | — | — | — | — |
| MobileSAM | Coffee | — | — | — | — | — | — |
| Mask2Former | Rice | — | — | — | — | — | — |
| Mask2Former | Coffee | — | — | — | — | — | — |

### Kết quả cần đạt cuối Phase 4

| Hạng mục | Mô tả |
|----------|-------|
| Best model sau tuning | 1 checkpoint final với hyperparams tối ưu, eval trên test set |
| Bảng before/after tuning | So sánh metrics trước và sau ASHA tuning |
| HuggingFace Hub | Final checkpoint public, dùng được qua HF Inference API |
| Notebook tuning | `tune_<model>_<dataset>.ipynb` đã chạy đầy đủ, có output ray[tune] |
| Báo cáo | Phần Tuning hoàn chỉnh với phân tích lỗi và kết luận chọn model |

---

## Đề xuất Điểm Sáng Tạo liên quan đến Model

| # | Ý tưởng sáng tạo | Phase | Người phụ trách | Giá trị mang lại |
|---|-----------------|-------|-----------------|-----------------|
| S2 | **Mask2Former fine-tune**: Transformer-based universal segmentation SOTA, fine-tune trên dataset lá cây Việt Nam | 3+4 | **Tuấn Anh** | Chiều sâu học thuật, áp dụng mô hình SOTA vào bài toán thực tế |
| S4 | **Instance Segmentation** thay vì classification: tạo masks thực địa, xác định vùng bệnh + nhãn cùng lúc *(đã xây dựng mask)* | 3+4 | **Tất cả** | Bài toán phong phú hơn, phù hợp ảnh thực địa nhiều lá |
| S5 | **RF-DETR Segmentation**: Detection Transformer của Roboflow, end-to-end fine-tuning | 3+4 | **Anh Tuấn** | Mô hình hiện đại, kết hợp detection + segmentation |

---

## Tổng hợp công việc (Model Phase)

| Thành viên | Phase 3 | Phase 4 | Sáng tạo |
|-----------|---------|---------|----------|
| **Lê Xuân Trí** | Mask R-CNN: train+eval ×2 datasets (3.1); **Hỗ trợ báo cáo Benchmark (3.9)** | **Hỗ trợ báo cáo Tuning — biểu đồ learning curve & RayTune (4.6)** | — |
| **Đàm Tiến Đạt** | MobileSAM: train+eval ×2 datasets (3.4); **Benchmark & chọn best model (3.6)** | **Setup RayTune+ASHA, Retrain, Evaluate & Push checkpoint (4.1–4.3)** | S4 |
| **Tống Thanh Phúc** | RF-DETR: train+eval ×2 datasets (3.3); **Viết báo cáo Benchmark (3.7)** | — | — |
| **Dương Tuấn Anh** | Mask2Former: train+eval ×2 datasets (3.5); **Hỗ trợ báo cáo Benchmark (3.8)** | **Hỗ trợ báo cáo Tuning — lý thuyết ASHA (4.5)** | S2 |
| **Nguyễn Hồ Anh Tuấn** | YOLO26-seg: train+eval ×2 datasets (3.2) | **Viết báo cáo Tuning — bảng before/after, phân tích (4.4)** | S5 |

---

## Checklist skeleton theo output (Model Phase)

| Phase | Output chính | Skeleton trong repo |
|---|---|---|
| 3 | Notebooks train+eval (Rice & Coffee) cho 5 model segmentation | `notebooks/models/mask_rcnn/{train_eval_rice,train_eval_coffee}.ipynb`, tương tự cho `yolo26_seg/`, `rf_detr/`, `mobilesam/`, `mask2former/` |
| 3 | Model checkpoints trên HuggingFace Hub (per-dataset) | README trong mỗi folder model ghi link HuggingFace |
| 4 | Notebook tuning best model bằng RayTune ASHA | `notebooks/models/<best_model>/tune_<dataset>.ipynb` |
| 4 | Final model checkpoint sau tuning | Checkpoint final trên HuggingFace Hub |

---

## Quy ước làm việc nhóm

- **Git workflow:** feature branch theo task → PR → review trước khi merge vào `main`
- **Họp nhóm:** ít nhất 1 lần/tuần để sync tiến độ, báo sớm blocker
- **Môi trường:** dùng chung `requirements.txt`, tạo virtual env riêng
- **Naming:** `notebooks/<phase>_<topic>_<author>.ipynb`; script đặt tên theo chức năng trong `src/`
- **Tracking:** cập nhật trạng thái task trong file này hoặc GitHub Issues
