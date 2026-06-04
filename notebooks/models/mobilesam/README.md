# Mobile SAM

## Code & Notebooks:

- [Code](https://github.com/magnusdtd/MobileSAM)
- Notebooks:
    - [Rice](https://www.kaggle.com/code/ducdamtien/ml-final-project-rice-mobilesam)
    - [Coffee](https://www.kaggle.com/code/ducdamtien/ml-final-project-coffee-mobilesam)
- [Checkpoints](https://huggingface.co/magnusdtd/ML-Final-Project-MobileSAM/tree/main)

## Charts:

### Training Metrics

| Dice Score | Epoch |
|:---:|:---:|
| ![Dice Score](imgs/Section-2-Panel-0-nxgdpzk24.png) | ![Epoch](imgs/Section-2-Panel-1-stn18v93y.png) |

| mAP@50 | mAP@50:95 |
|:---:|:---:|
| ![mAP@50](imgs/Section-2-Panel-2-2baaw13s7.png) | ![mAP@50:95](imgs/Section-2-Panel-3-wlem76bo9.png) |

| mIoU | Learning Rate |
|:---:|:---:|
| ![mIoU](imgs/Section-2-Panel-4-y6lo2osp3.png) | ![Learning Rate](imgs/Section-2-Panel-5-yxi3b8u8d.png) |

| Training Loss | Validation Loss |
|:---:|:---:|
| ![Training Loss](imgs/Section-2-Panel-6-en5u6a18q.png) | ![Validation Loss](imgs/Section-2-Panel-7-jknxguce4.png) |

### System Metrics

| GPU Utilization (%) | GPU Temperature (°C) |
|:---:|:---:|
| ![GPU Utilization](imgs/Section-5-Panel-0-74osjbms2.png) | ![GPU Temperature](imgs/Section-5-Panel-1-0i1jixshp.png) |

| GPU Power Usage (W) | GPU Power Usage (%) |
|:---:|:---:|
| ![GPU Power Usage (W)](imgs/Section-5-Panel-2-78taxunmb.png) | ![GPU Power Usage (%)](imgs/Section-5-Panel-3-y5v9g5dxo.png) |

| GPU Enforced Power Limit (W) | GPU SM Clock Speed (MHz) |
|:---:|:---:|
| ![GPU Enforced Power Limit](imgs/Section-5-Panel-4-9a8p3ca8p.png) | ![GPU SM Clock Speed](imgs/Section-5-Panel-5-rjd49umbb.png) |

| GPU Memory Clock Speed (MHz) | GPU Memory Allocated (Bytes) |
|:---:|:---:|
| ![GPU Memory Clock Speed](imgs/Section-5-Panel-6-xdm1pxsfa.png) | ![GPU Memory Allocated (Bytes)](imgs/Section-5-Panel-7-hsoa6a1yt.png) |

| GPU Memory Allocated (%) | GPU Time Spent Accessing Memory (%) |
|:---:|:---:|
| ![GPU Memory Allocated (%)](imgs/Section-5-Panel-8-4gqxp5t9y.png) | ![GPU Time Accessing Memory](imgs/Section-5-Panel-9-yn8icvt86.png) |

| GPU Corrected Memory Errors | GPU Uncorrected Memory Errors |
|:---:|:---:|
| ![GPU Corrected Memory Errors](imgs/Section-5-Panel-10-akfmbyhzr.png) | ![GPU Uncorrected Memory Errors](imgs/Section-5-Panel-11-5c22372mh.png) |

| Network Traffic (Bytes) | Disk Utilization (GB) |
|:---:|:---:|
| ![Network Traffic](imgs/Section-5-Panel-12-ym07kfi9y.png) | ![Disk Utilization (GB)](imgs/Section-5-Panel-13-3uj52gb97.png) |

| Disk Utilization (%) | Disk I/O Utilization (MB) |
|:---:|:---:|
| ![Disk Utilization (%)](imgs/Section-5-Panel-14-ux1tjf80a.png) | ![Disk I/O Utilization](imgs/Section-5-Panel-15-lwaxxsedd.png) |

| Process CPU Utilization (%) | Process CPU Threads In Use |
|:---:|:---:|
| ![Process CPU Utilization](imgs/Section-5-Panel-16-24kfmi7qt.png) | ![Process CPU Threads](imgs/Section-5-Panel-17-b18qxmh4k.png) |

| Process Memory In Use (MB) | Process Memory In Use (%) |
|:---:|:---:|
| ![Process Memory (MB)](imgs/Section-5-Panel-18-ugfjy3x68.png) | ![Process Memory (%)](imgs/Section-5-Panel-19-wj4gdlag6.png) |

| Process Memory Available (MB) | System Memory Utilization (%) |
|:---:|:---:|
| ![Process Memory Available](imgs/Section-5-Panel-20-8nvaczl54.png) | ![System Memory Utilization](imgs/Section-5-Panel-21-rzjwc9jov.png) |

## Results:

| Model Type | mAP@50 | mAP@50:95 | mIoU | Dice | Inference (ms) | Size (MB) |
|---------|--------|-----------|------|------|----------------|-----------|
| Rice MobileSAM (PyTorch) | 0.5637 | 0.5141 | 0.5440 | 0.5712 | 65.90 | 41.3 |
| Rice MobileSAM (ONNX) | 0.5637 | 0.5141 | 0.5440 | 0.5712 | 160.24 | 17.1 |
| Rice MobileSAM (ONNX Quantized) | 0.5469 | 0.5008 | 0.5315 | 0.5589 | 166.07 | 8.96 |
| Coffee MobileSAM (PyTorch) | 0.6923 | 0.6591 | 0.6671 | 0.6848 | 62.14 | 41.3 |
| Coffee MobileSAM (ONNX) | 0.6923 | 0.6591 | 0.6671 | 0.6848 | 146.31 | 17.1 |
| Coffee MobileSAM (ONNX Quantized) | 0.6923 | 0.6559 | 0.6639 | 0.6820 | 148.13 | 8.96 |
