# YOLO26m-seg Tuning & Inference Pipeline

This repository contains the complete pipeline to train, tune, quantize, and run inference for the **YOLO26m-seg** instance segmentation model, specifically applied to Vietnamese Rice and Coffee Leaf Disease datasets. 

This README focuses on **running inference with the trained 8-bit ONNX version (INT8)**, which provides significant speedups and memory footprint reductions for CPU-based deployment while preserving segmentation accuracy.

Links:
- [Hyperparameter Tuning Notebook](https://www.kaggle.com/code/ducdamtien/ml-final-project-ray-tune)
- [Train Notebook](https://www.kaggle.com/code/ducdamtien/ml-final-project-yolo)
- [HF repo](https://huggingface.co/magnusdtd/ML-Final-Project-YOLO26seg-RayTune)

---

## 🚀 Running Inference with 8-bit ONNX (INT8)

The standalone ONNX inference implementation is provided in [`yolo26seg_onnx.py`](yolo26seg_onnx.py). This script performs inference directly using ONNX Runtime, eliminating the need for PyTorch or Ultralytics as runtime dependencies. It handles all necessary pre-processing (letterboxing, normalization) and post-processing (NMS, mask generation, scaling).

### Requirements

To run the INT8 ONNX model, you only need the following lightweight dependencies:

```bash
uv add onnxruntime opencv-python numpy
```

### Usage

You can use the `run_inference` function to detect bounding boxes and segmentation masks from an image. 

```python
import cv2
from yolo26seg_onnx import run_inference

# Path to your quantized INT8 model
model_path = "best_yolo26m_seg_rice_int8.onnx"
image_path = "test_image.jpg"

# Run inference
boxes, masks = run_inference(model_path, image_path, conf_threshold=0.25)

print(f"Detected {len(boxes)} object(s).")

# `boxes` format: [[x1, y1, x2, y2, confidence, class_id], ...] (scaled to original image size)
# `masks` format: List of binary masks (numpy arrays) matching original image dimensions
```

If you want to run the script directly from the command line for a quick test:
```bash
uv run yolo26seg_onnx.py
```
*(Make sure to update the model and image paths at the bottom of the script).*

---
