# RF-DETR Segmentation

Thư mục này chứa notebook train/evaluate RF-DETR segmentation cho bài toán phát hiện bệnh lá cà phê và lúa. Hiện tại pipeline đã tách thành hai notebook riêng:

- `train-eva-coffee.ipynb`: train/evaluate model cho coffee.
- `train-eva-rice.ipynb`: train/evaluate model cho rice.
- `mining-data.ipynb`: notebook đã dùng để kiểm tra cấu trúc raw dataset trên Kaggle.
- `explore_raw_data.ipynb`: notebook EDA raw data, có thể chạy lại nếu cần kiểm tra dataset.
- `train_evaluate_tune.ipynb`, `train_evaluate_tune_coffee.ipynb`, `train_evaluate_tune_rice.ipynb`: notebook cũ, chỉ giữ lại để tham khảo.

## Raw Data Trên Kaggle

Theo kết quả từ `mining-data.ipynb`, raw dataset được mount trên Kaggle tại:

```text
/kaggle/input/datasets/magnusdtd2/rice-coffee-leaf-disease/
|-- coffee_leaf_disease/
|   |-- 0/
|   |-- 1/
|   |-- 2/
|   |-- 3/
|   `-- annotations.coco.json
`-- rice_leaf_disease/
    |-- BrownSpot/
    |-- Healthy/
    |-- Hispa/
    |-- LeafBlast/
    `-- annotations.coco.json
```

Nếu Kaggle mount dataset ở đường dẫn khác, đặt biến môi trường `RAW_DATA_DIR` trỏ tới thư mục chứa `coffee_leaf_disease/` và/hoặc `rice_leaf_disease/`.

Notebook cũng tự dò thêm một số đường dẫn phổ biến như:

```text
/kaggle/input/datasets/tongthanhphuc/cafe-rice
/kaggle/input/rice-coffee-leaf-disease
/kaggle/input/cafe-rice
/kaggle/input/cafe_rice
/kaggle/input/coffee-rice
```

## Kết Quả Mining Data

Coffee:

- COCO images: `3879`
- COCO annotations: `3842`
- COCO categories: `5`
- Physical images: `3879`
- Resolved images: `3879`
- Unresolved images: `0`
- Images without annotations: `37`
- Images with annotations: `3842`
- Raw category phụ/không hợp lệ: `uit` / `none`

Rice:

- COCO images: `3421`
- COCO annotations: `3720`
- COCO categories: `4`
- Physical images: `3421`
- Resolved images: `3421`
- Unresolved images: `0`
- Images without annotations: `5`
- Images with annotations: `3416`
- Một số ảnh có nhiều annotation, tối đa `28` annotation/ảnh.

## Mapping Nhãn

Coffee raw COCO dùng folder/category id dạng số. Notebook map về nhãn sạch:

- `0` -> `LeafMiner`
- `1` -> `PowderyMildew`
- `2` -> `Rust`
- `3` -> `AlgalLeafSpot`

Các nhãn invalid/background như `uit`, `none`, nhãn rỗng, `invalid`, `background`, `__background__` sẽ bị bỏ qua trước khi tạo dataset RF-DETR.

Rice raw COCO đã có nhãn rõ:

- `BrownSpot`
- `Healthy`
- `Hispa`
- `LeafBlast`

## Dữ Liệu Raw Và Processed

Nguồn train chính là raw COCO:

- `coffee_leaf_disease/annotations.coco.json`
- `rice_leaf_disease/annotations.coco.json`

Ngoài raw data, notebook có thể dùng thêm dữ liệu trong `processed/` nếu tìm thấy `processed/metadata/*.csv`.

Chi tiết:

- Raw COCO dùng bbox/mask thật trong `annotations.coco.json`.
- Processed data được đọc từ manifest CSV.
- Vì `processed/` không có COCO mask vùng bệnh, notebook tạo pseudo full-image annotation cho ảnh processed.
- Có thể tắt dữ liệu processed bằng:

```text
USE_PROCESSED_EXTRA=0
```

- `processed/metadata` cũng được dùng để hỗ trợ suy luận mapping `class_folder -> label` cho coffee nếu có sẵn.

## Pipeline Chính

Mỗi notebook `train-eva-*.ipynb` thực hiện các bước:

1. Tìm raw root trên Kaggle.
2. Đọc COCO raw của domain tương ứng.
3. Inspect raw COCO trước khi train.
4. Resolve đường dẫn ảnh.
5. Bỏ ảnh không có annotation hợp lệ.
6. Bỏ annotation invalid/background.
7. Giữ multi-annotation, đặc biệt quan trọng với rice.
8. Nếu bật `USE_PROCESSED_EXTRA`, nạp thêm ảnh processed theo manifest và tạo pseudo full-image annotation.
9. Remap category id về class riêng của domain.
10. Chia raw data theo tỷ lệ `70/15/15` cho train/valid/test.
11. Giữ split có sẵn của processed data nếu manifest cung cấp split.
12. Ghi dataset RF-DETR vào `/kaggle/working/rfdetr_datasets/<domain>`.
13. Validate COCO output, đảm bảo không còn label invalid như `uit`.
14. Train một config duy nhất.
15. Evaluate trên test set bằng checkpoint tốt nhất.
16. Lưu checkpoint, metrics, prediction JSON, confusion matrix, learning/result plot và model card.

## Config Train

Mỗi domain chạy một config:

```python
TRAIN_CONFIG = {
    "name": "train_lr1e4",
    "model_size": DEFAULT_MODEL_SIZE,
    "epochs": 2 if QUICK_RUN else 8,
    "batch_size": 2 if QUICK_RUN else 4,
    "grad_accum_steps": 8 if QUICK_RUN else 4,
    "lr": 1e-4,
    "lr_encoder": 1.5e-4,
    "gradient_checkpointing": True,
    "early_stopping": True,
    "early_stopping_patience": 2 if QUICK_RUN else 5,
}
```

Mặc định model size:

```text
RFDETR_MODEL_SIZE=nano
```

Chạy smoke test nhanh:

```text
QUICK_RUN=1
```

Tắt train, chỉ chạy các cell sau nếu đã có artifact phù hợp:

```text
RUN_TRAINING=0
```

Tắt evaluate:

```text
RUN_EVALUATION=0
```

## Output

Artifact chính được lưu tại:

```text
/kaggle/working/rf_detr_artifacts/
|-- coffee/
|   |-- best.pt
|   |-- result.csv
|   |-- result.png
|   |-- confusion_matrix.csv
|   |-- confusion_matrix.png
|   |-- test_classification_metrics.csv
|   |-- metrics_train_lr1e4.csv
|   |-- per_image_errors_train_lr1e4.csv
|   |-- train_lr1e4/
|   `-- best_model/
`-- rice/
    |-- best.pt
    |-- result.csv
    |-- result.png
    |-- confusion_matrix.csv
    |-- confusion_matrix.png
    |-- test_classification_metrics.csv
    |-- metrics_train_lr1e4.csv
    |-- per_image_errors_train_lr1e4.csv
    |-- train_lr1e4/
    `-- best_model/
```

Ngoài ra, prediction JSON được lưu ở:

```text
/kaggle/working/rf_detr_artifacts/predictions_<domain>_train_lr1e4_test.json
/kaggle/working/rf_detr_artifacts/rf_detr_domain_metrics.csv
```

Trong `best_model/` có các file dùng để upload Hugging Face:

- `best.pt`: checkpoint tốt nhất.
- `class_names.json`: mapping category id -> tên class.
- `metrics.csv`: metrics của run train.
- `config.json`: metadata và train config.
- `README.md`: model card sinh tự động.
- `result.csv`: log learning curve nếu đọc được từ TensorBoard/CSV; nếu không có log epoch thì lưu metric cuối cùng.
- `result.png`: biểu đồ learning curve hoặc biểu đồ metric cuối cùng.
- `confusion_matrix.csv`: confusion matrix dạng bảng.
- `confusion_matrix.png`: ảnh confusion matrix.
- `test_classification_metrics.csv`: precision, recall, F1 theo class với ngưỡng IoU `0.5`.

Metrics evaluate chính gồm:

- `mAP50_bbox`
- `mAP50_95_bbox`
- `mAP50_segm`
- `mAP50_95_segm`
- `mIoU`
- `Dice`
- `inference_ms_per_image`

## Kết Quả Test Đã Chạy

Các kết quả dưới đây được lấy từ output đã lưu trong hai notebook `train-eva-coffee.ipynb` và `train-eva-rice.ipynb`. Cả hai đều evaluate trên split `test` với config `train_lr1e4`.

| Domain | Test images | mAP50_bbox | mAP50_95_bbox | mAP50_segm | mAP50_95_segm | mIoU | Dice | Inference ms/image |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| coffee | 576 | 0.820 | 0.598 | 0.842835 | 0.825083 | 0.857505 | 0.871758 | 70.306413 |
| rice | 514 | 0.736 | 0.718 | 0.703828 | 0.687440 | 0.813240 | 0.830791 | 198.306173 |

Với bài toán segmentation, hai chỉ số nên báo cáo chính là:

- `mAP50_segm`
- `mAP50_95_segm`

Các file chứa kết quả test sau khi chạy notebook:

```text
/kaggle/working/rf_detr_artifacts/coffee/metrics_train_lr1e4.csv
/kaggle/working/rf_detr_artifacts/rice/metrics_train_lr1e4.csv
/kaggle/working/rf_detr_artifacts/rf_detr_domain_metrics.csv
/kaggle/working/rf_detr_artifacts/coffee/best_model/metrics.csv
/kaggle/working/rf_detr_artifacts/rice/best_model/metrics.csv
```

## Upload Hugging Face

Hai notebook có cell upload artifact `best_model/` lên Hugging Face Hub.

Biến mặc định:

```text
RUN_HF_PUSH=1
HF_REPO_ID=fuxi611/coffee-rice-leaf-disease-rf-detr
HF_UPLOAD_SINGLE_REPO=1
```

Cần thêm Kaggle Secret hoặc environment variable:

```text
HF_TOKEN=<huggingface_write_token>
```

Khi `HF_UPLOAD_SINGLE_REPO=1`, cả hai model được upload vào cùng một repo, tách theo thư mục:

```text
fuxi611/coffee-rice-leaf-disease-rf-detr/
  coffee/
    best.pt
    class_names.json
    metrics.csv
    config.json
    README.md
    result.csv
    result.png
    confusion_matrix.csv
    confusion_matrix.png
    test_classification_metrics.csv
  rice/
    best.pt
    class_names.json
    metrics.csv
    config.json
    README.md
    result.csv
    result.png
    confusion_matrix.csv
    confusion_matrix.png
    test_classification_metrics.csv
```

Nếu muốn upload thành hai repo riêng, đặt:

```text
HF_UPLOAD_SINGLE_REPO=0
```

Khi đó nếu `HF_REPO_ID=<owner>/<repo-prefix>`, notebook sẽ dùng:

```text
<owner>/<repo-prefix>-coffee
<owner>/<repo-prefix>-rice
```

## Cách Chạy Trên Kaggle

Khuyến nghị chạy lần lượt:

1. `train-eva-coffee.ipynb`
2. `train-eva-rice.ipynb`

Không nên chạy song song hai notebook trên cùng một GPU Kaggle vì dễ thiếu VRAM hoặc bị chậm.

Trước khi chạy:

- Bật GPU.
- Bật Internet nếu cần cài package hoặc upload Hugging Face.
- Add dataset raw vào Kaggle input.
- Thêm Kaggle Secret `HF_TOKEN` nếu muốn upload model.

## Ghi Chú

Hai notebook `train-eva-coffee.ipynb` và `train-eva-rice.ipynb` được viết dựa trên kết quả inspect từ `mining-data.ipynb`, thay vì đoán cấu trúc raw data. Nếu raw dataset trên Kaggle thay đổi, hãy chạy lại `mining-data.ipynb` trước rồi cập nhật mapping/path trong notebook tương ứng.
