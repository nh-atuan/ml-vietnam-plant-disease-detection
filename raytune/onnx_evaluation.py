import os
import sys
import time
import shutil
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image
import torch

from ultralytics import YOLO
import onnxruntime as ort
from onnxruntime.quantization import QuantType, quantize_dynamic

from yolo26seg import (
    rasterize_label_file,
    rasterize_predictions,
    mean_iou_dice,
    extract_ultralytics_metrics
)

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114)):
    """Resizes and pads image to maintain aspect ratio without distortion."""
    shape = im.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2

    if shape[::-1] != new_unpad:
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)

    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return im, r, (left, top), new_unpad

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def run_inference_ort(session, image_path, conf_threshold=0.25, imgsz=640):
    """Direct ONNX Runtime inference implementation matching yolo26seg_onnx.py."""
    input_name = session.get_inputs()[0].name
    img_size = (imgsz, imgsz)

    orig_img = cv2.imread(str(image_path))
    if orig_img is None:
        raise ValueError(f"Could not load image: {image_path}")
    orig_h, orig_w = orig_img.shape[:2]
    input_img, ratio, (pad_w, pad_h), new_unpad = letterbox(orig_img, img_size)

    # BGR to RGB -> HWC to CHW -> Normalize -> Add batch dimension
    blob = input_img[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0

    # Run direct inference
    outputs = session.run(None, {input_name: blob})
    preds = outputs[0][0]
    protos = outputs[1][0]

    keep = preds[:, 4] > conf_threshold
    preds = preds[keep]

    if len(preds) == 0:
        return [], []

    boxes = preds[:, :4]
    confs = preds[:, 4]
    class_ids = preds[:, 5]
    coeffs = preds[:, 6:]  # Extract the 32 mask coefficients: shape (N, 32)

    # Segmentation Mask Post-Processing
    num_masks = len(preds)
    protos_flat = protos.reshape(32, -1)
    raw_masks = sigmoid(coeffs @ protos_flat).reshape(num_masks, 160, 160)

    final_masks = []
    final_boxes = []

    for i in range(num_masks):
        # Scale 160x160 resolution up to the 640x640 input resolution
        mask_640 = cv2.resize(raw_masks[i], img_size, interpolation=cv2.INTER_LINEAR)

        # Crop away the letterbox padding
        mask_cropped = mask_640[pad_h : pad_h + new_unpad[1], pad_w : pad_w + new_unpad[0]]

        # Resize to match original image dimensions & apply threshold
        mask_orig = cv2.resize(mask_cropped, (orig_w, orig_h), interpolation=cv2.INTER_LINEAR)
        binary_mask = (mask_orig > 0.5).astype(np.uint8)

        # Map box coordinates back to original image scale
        x1 = int((boxes[i][0] - pad_w) / ratio)
        y1 = int((boxes[i][1] - pad_h) / ratio)
        x2 = int((boxes[i][2] - pad_w) / ratio)
        y2 = int((boxes[i][3] - pad_h) / ratio)

        # Clip coordinates to image boundary
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(orig_w, x2), min(orig_h, y2)

        # Eliminate edge artifacts by cropping mask strictly to its bounding box
        box_mask = np.zeros_like(binary_mask)
        box_mask[y1:y2, x1:x2] = 1
        binary_mask = binary_mask * box_mask

        final_masks.append(binary_mask)
        final_boxes.append([x1, y1, x2, y2, confs[i], int(class_ids[i])])

    return final_boxes, final_masks

def rasterize_ort_predictions(boxes, masks, width: int, height: int, domain_classes: list[str]) -> np.ndarray:
    """Rasterize custom ONNX Runtime predictions into a class-wise binary mask."""
    pred_masks = np.zeros((len(domain_classes), height, width), dtype=bool)
    if not boxes or not masks:
        return pred_masks
    for box, mask in zip(boxes, masks):
        class_id = int(box[5])
        if not 0 <= class_id < len(domain_classes):
            continue
        mask_bool = mask > 0.5
        if mask_bool.shape != (height, width):
            mask_img = Image.fromarray(mask_bool.astype(np.uint8) * 255).resize(
                (width, height), Image.Resampling.NEAREST
            )
            mask_bool = np.asarray(mask_img, dtype=np.uint8) > 0
        pred_masks[class_id] |= mask_bool
    return pred_masks

def export_and_quantize_models(pt_path: Path, output_dir: Path, imgsz: int = 640):
    """Export the trained PyTorch model to FP32, FP16, INT8, INT4, and INT2 ONNX."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print(f"Loading PyTorch model from {pt_path}...")
    print("=" * 80)
    model = YOLO(str(pt_path), task="segment")

    # 1. Export standard FP32 ONNX
    print("Exporting FP32 ONNX model...")
    fp32_temp_path = Path(model.export(format="onnx", imgsz=imgsz, opset=12))
    fp32_path = output_dir / f"{pt_path.stem}.onnx"
    if fp32_temp_path.exists():
        if fp32_temp_path != fp32_path:
            shutil.move(str(fp32_temp_path), str(fp32_path))
        print(f"Successfully exported FP32 ONNX to {fp32_path}")
    else:
        raise RuntimeError("FP32 ONNX export failed.")

    # 2. Export FP16 ONNX
    print("Exporting FP16 ONNX model...")
    fp16_path = output_dir / f"{pt_path.stem}_fp16.onnx"
    try:
        # Move FP32 temporarily so YOLO half=True export doesn't overwrite it if it outputs to default path
        temp_fp32 = fp32_path.with_name("best_temp.onnx")
        if fp32_path.exists():
            fp32_path.rename(temp_fp32)
            
        fp16_temp_path = Path(model.export(format="onnx", imgsz=imgsz, opset=12, half=True))
        if fp16_temp_path.exists():
            shutil.move(str(fp16_temp_path), str(fp16_path))
            
            # --- FIX FOR DUPLICATE NODE NAMES IN FP16 ONNX ---
            try:
                import onnx
                import onnxslim
                model_fp16 = onnxslim.slim(str(fp16_path))
                
                # Clear node names to fix 'two nodes with same node name'
                for node in model_fp16.graph.node:
                    if node.name:
                        node.name = ""
                        
                # Aggressively deduplicate value_infos
                seen_vi = set()
                new_vi = []
                for vi in model_fp16.graph.value_info:
                    if vi.name not in seen_vi:
                        seen_vi.add(vi.name)
                        new_vi.append(vi)
                del model_fp16.graph.value_info[:]
                model_fp16.graph.value_info.extend(new_vi)
                
                onnx.save(model_fp16, str(fp16_path))
            except Exception as e:
                print(f"Failed to fix duplicate nodes in FP16 ONNX: {e}")
            # -------------------------------------------------

            print(f"Successfully exported FP16 ONNX to {fp16_path}")
        else:
            print("Error: FP16 ONNX temp file not found.")
            
        if temp_fp32.exists():
            temp_fp32.rename(fp32_path)
    except Exception as e:
        print(f"Error exporting FP16 ONNX: {e}")

    # 3. Quantize the ONNX model to INT8 (Dynamic)
    print("Quantizing ONNX model to INT8 (Dynamic)...")
    int8_path = output_dir / f"{pt_path.stem}_int8.onnx"
    try:
        quantize_dynamic(
            model_input=str(fp32_path),
            model_output=str(int8_path),
            weight_type=QuantType.QUInt8
        )
        print(f"Successfully quantized ONNX model to INT8: {int8_path}")
    except Exception as e:
        print(f"Error during ONNX INT8 dynamic quantization: {e}")

    # Helper function for N-Bits Weight-Only Quantization
    def quantize_weight_only(bits, output_path):
        quantizer = None
        
        # Try newest API (ONNX Runtime >= 1.20)
        try:
            from onnxruntime.quantization import MatMulNBitsQuantizer
            try:
                from onnxruntime.quantization.calibrate import WeightOnlyQuantConfig
                quant_config = WeightOnlyQuantConfig(bits=bits, block_size=128, is_symmetric=True)
                quantizer = MatMulNBitsQuantizer(str(fp32_path), algo_config=quant_config)
            except Exception:
                # Fallback if WeightOnlyQuantConfig is unavailable or has different args
                quantizer = MatMulNBitsQuantizer(str(fp32_path), bits=bits, block_size=128, is_symmetric=True)
        except ImportError:
            pass

        # Try older unified API (ONNX Runtime 1.17 - 1.19)
        if quantizer is None:
            try:
                from onnxruntime.quantization.matmul_nbits_quantizer import MatMulNBitsQuantizer
                quantizer = MatMulNBitsQuantizer(
                    model=str(fp32_path),
                    bits=bits,
                    block_size=128,
                    is_symmetric=True
                )
            except ImportError:
                pass

        # Try oldest API (ONNX Runtime <= 1.16)
        if quantizer is None:
            if bits == 4:
                from onnxruntime.quantization.matmul_4bits_quantizer import MatMul4BitsQuantizer
                quantizer = MatMul4BitsQuantizer(
                    model=str(fp32_path),
                    block_size=128,
                    is_symmetric=True
                )
            elif bits == 2:
                from onnxruntime.quantization.matmul_4bits_quantizer import MatMul2BitsQuantizer
                quantizer = MatMul2BitsQuantizer(
                    model=str(fp32_path),
                    block_size=128,
                    is_symmetric=True
                )
            else:
                raise ValueError(f"Unsupported bits: {bits}")
        
        quantizer.process()
        quantizer.model.save_model_to_file(str(output_path), use_external_data_format=False)

    # 4. Quantize to INT4 (Block-wise Weight-Only)
    print("Quantizing ONNX model to INT4...")
    int4_path = output_dir / f"{pt_path.stem}_int4.onnx"
    try:
        quantize_weight_only(bits=4, output_path=int4_path)
        print(f"Successfully quantized ONNX model to INT4: {int4_path}")
    except Exception as e:
        print(f"Error during ONNX INT4 quantization: {e}")

    # 5. Quantize to INT2 (Block-wise Weight-Only)
    print("Quantizing ONNX model to INT2...")
    int2_path = output_dir / f"{pt_path.stem}_int2.onnx"
    try:
        quantize_weight_only(bits=2, output_path=int2_path)
        print(f"Successfully quantized ONNX model to INT2: {int2_path}")
    except Exception as e:
        print(f"Error during ONNX INT2 quantization: {e}")

    return {
        "pt": pt_path,
        "fp32": fp32_path,
        "fp16": fp16_path,
        "int8": int8_path,
        "int4": int4_path,
        "int2": int2_path
    }

def benchmark_latency(
    model_path: Path, 
    df: pd.DataFrame, 
    imgsz: int = 640, 
    device: str = "cpu", 
    n_images: int = 50,
) -> float:
    """Benchmark inference latency (ms) for either a PyTorch (.pt) or ONNX (.onnx) model."""
    test_paths = [Path(p) for p in df[df["split"] == "test"]["image_path_yolo"].head(n_images)]
    if not test_paths:
        return float("nan")

    if model_path.suffix == ".pt":
        model = YOLO(str(model_path), task="segment")
        # Warmup
        for p in test_paths[:3]:
            model.predict(str(p), imgsz=imgsz, device=device, verbose=False)
        # Benchmark
        start = time.perf_counter()
        for p in test_paths:
            model.predict(str(p), imgsz=imgsz, device=device, verbose=False)
        elapsed = time.perf_counter() - start
    else:
        # ONNX model evaluation using ONNX Runtime
        providers = ["CPUExecutionProvider"] if device == "cpu" else ["CUDAExecutionProvider"]
        try:
            session = ort.InferenceSession(str(model_path), providers=providers)
        except Exception as e:
            print(f"Warning: Failed to create ORT InferenceSession on {device} for {model_path.name}: {e}")
            return float("nan")
        
        # Warmup
        for p in test_paths[:3]:
            run_inference_ort(session, p, imgsz=imgsz)
        # Benchmark
        start = time.perf_counter()
        for p in test_paths:
            run_inference_ort(session, p, imgsz=imgsz)
        elapsed = time.perf_counter() - start

    return elapsed * 1000.0 / len(test_paths)

def evaluate_model(
    model_name: str,
    model_path: Path,
    df: pd.DataFrame,
    domain_classes: list[str],
    data_yaml: Path,
    imgsz: int = 640,
    device_gpu: str = "0"
) -> dict:
    """Run full validation, custom metrics, size, and CPU/GPU latency evaluations."""
    print(f"\nEvaluating {model_name} ({model_path.name})...")
    
    # 1. Model Size (MB)
    size_mb = model_path.stat().st_size / (1024 * 1024) if model_path.exists() else float("nan")
    
    # 2. CPU Latency Benchmark
    print(" - Benchmarking CPU latency...")
    cpu_latency = benchmark_latency(model_path, df, imgsz=imgsz, device="cpu")

    # 3. GPU Latency Benchmark (if GPU/CUDA is available)
    gpu_latency = float("nan")
    if torch.cuda.is_available():
        print(" - Benchmarking GPU latency...")
        gpu_latency = benchmark_latency(model_path, df, imgsz=imgsz, device=device_gpu)
    
    # 4. Standard YOLO mAP metrics (if supported/works)
    map50 = float("nan")
    map95 = float("nan")
    try:
        model = YOLO(str(model_path), task="segment")
        val_metrics = model.val(
            data=str(data_yaml),
            split="test",
            imgsz=imgsz,
            device="cpu", # Default to CPU validation to avoid CUDA resource conflicts
            plots=False,
            verbose=False,
            task="segment"
        )
        yolo_metrics = extract_ultralytics_metrics(val_metrics)
        map50 = yolo_metrics.get("mAP50_mask", float("nan"))
        map95 = yolo_metrics.get("mAP50_95_mask", float("nan"))
    except Exception as e:
        print(f" - Note: YOLO native val() skipped/failed for {model_path.name}: {e}")

    # 5. Semantic overlap metrics (mIoU and Dice Score)
    # Use direct ORT session for ONNX models to be robust, YOLO for PyTorch
    print(" - Computing mIoU & Dice Score on test split...")
    split_df = df[df["split"] == "test"].copy()
    ious = []
    dices = []
    
    if model_path.suffix == ".pt":
        model = YOLO(str(model_path), task="segment")
        for _, row in split_df.iterrows():
            image_path = Path(row["image_path_yolo"])
            image = Image.open(image_path).convert("RGB")
            width, height = image.size
            gt = rasterize_label_file(Path(row["label_path"]), width, height, domain_classes)
            result = model.predict(str(image_path), imgsz=imgsz, device="cpu", verbose=False)[0]
            pred = rasterize_predictions(result, width, height, domain_classes)
            miou, dice, _, _, _ = mean_iou_dice(gt, pred, domain_classes)
            ious.append(miou)
            dices.append(dice)
    else:
        # Load via ONNX Runtime directly
        try:
            session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
            for _, row in split_df.iterrows():
                image_path = Path(row["image_path_yolo"])
                image = Image.open(image_path).convert("RGB")
                width, height = image.size
                gt = rasterize_label_file(Path(row["label_path"]), width, height, domain_classes)
                boxes, masks = run_inference_ort(session, image_path, imgsz=imgsz)
                pred = rasterize_ort_predictions(boxes, masks, width, height, domain_classes)
                miou, dice, _, _, _ = mean_iou_dice(gt, pred, domain_classes)
                ious.append(miou)
                dices.append(dice)
        except Exception as e:
            print(f" - Error: direct ORT metric computation failed for {model_path.name}: {e}")
            
    miou = float(np.mean(ious)) if ious else float("nan")
    dice = float(np.mean(dices)) if dices else float("nan")

    return {
        "Model": model_name,
        "Size (MB)": size_mb,
        "mIoU": miou,
        "Dice Score": dice,
        "mAP@50": map50,
        "mAP@50-90": map95,
        "CPU Latency (ms)": cpu_latency,
        "GPU Latency (ms)": gpu_latency
    }

def run_evaluation_pipeline(
    pt_path: Path, 
    df: pd.DataFrame, 
    domain_classes: list[str], 
    data_yaml: Path, 
    output_dir: Path, 
    imgsz: int = 640,
):
    """Export, quantize, evaluate all 6 versions, and output the comparison table."""
    print("Starting export, quantization, and evaluation pipeline for all model versions...")
    
    # 1. Export and Quantize
    model_paths = export_and_quantize_models(pt_path, output_dir, imgsz=imgsz)
    
    # 2. Evaluate all models
    results = []
    models_to_eval = [
        ("PyTorch", model_paths["pt"]),
        ("ONNX FP32", model_paths["fp32"]),
        ("ONNX FP16", model_paths["fp16"]),
        ("ONNX INT8", model_paths["int8"]),
        ("ONNX INT4", model_paths["int4"]),
        ("ONNX INT2", model_paths["int2"])
    ]
    
    gpu_device = "0" if torch.cuda.is_available() else "cpu"
    
    for name, path in models_to_eval:
        if path and path.exists():
            metrics = evaluate_model(
                model_name=name,
                model_path=path,
                df=df,
                domain_classes=domain_classes,
                data_yaml=data_yaml,
                imgsz=imgsz,
                device_gpu=gpu_device
            )
            results.append(metrics)
        else:
            print(f"\nSkipping evaluation of {name} (file not found).")
            
    # 3. Create DataFrame and display Markdown comparison
    summary_df = pd.DataFrame(results)
    
    # Clean up formatting for display
    summary_df["Size (MB)"] = summary_df["Size (MB)"].map(lambda x: f"{x:.2f}" if not np.isnan(x) else "N/A")
    for metric_col in ["mIoU", "Dice Score", "mAP@50", "mAP@50-90"]:
        summary_df[metric_col] = summary_df[metric_col].map(lambda x: f"{x:.4f}" if not np.isnan(x) else "N/A")
    for latency_col in ["CPU Latency (ms)", "GPU Latency (ms)"]:
        summary_df[latency_col] = summary_df[latency_col].map(lambda x: f"{x:.2f}" if not np.isnan(x) else "N/A")

    print("\n" + "=" * 80)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 80)
    markdown_table = summary_df.to_markdown(index=False)
    print(markdown_table)
    print("=" * 80)
    
    # Save comparison report to disk
    report_csv = output_dir / "onnx_quantization_comparison.csv"
    summary_df.to_csv(report_csv, index=False)
    print(f"Saved comparison report to: {report_csv}")
    
    # Save markdown summary table as a README note in the artifacts directory
    report_md = output_dir / "onnx_quantization_report.md"
    report_md.write_text(f"## ONNX Export & Quantization Metrics Comparison\n\n{markdown_table}\n", encoding="utf-8")
    print(f"Saved markdown report to: {report_md}")

    return summary_df
