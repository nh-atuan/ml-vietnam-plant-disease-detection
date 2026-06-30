import cv2
import numpy as np
import onnxruntime as ort


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


def run_inference(model_path, image_path, conf_threshold=0.25):

    session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape  # [1, 3, 640, 640]
    img_size = (input_shape[3], input_shape[2])

    orig_img = cv2.imread(image_path)
    orig_h, orig_w = orig_img.shape[:2]
    input_img, ratio, (pad_w, pad_h), new_unpad = letterbox(orig_img, img_size)

    # BGR to RGB -> HWC to CHW -> Normalize -> Add batch dimension
    blob = input_img[..., ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255.0

    # YOLO26-seg returns two outputs:
    # output0: (1, 300, 38) -> [x1, y1, x2, y2, conf, class_id + 32 mask coefficients]
    # output1: (1, 32, 160, 160) -> Mask prototypes (proto)
    outputs = session.run(None, {input_name: blob})
    preds = outputs[0][0]
    protos = outputs[1][0]

    keep = preds[:, 4] > conf_threshold
    preds = preds[keep]

    if len(preds) == 0:
        print("No objects detected.")
        return [], []

    boxes = preds[:, :4]
    confs = preds[:, 4]
    class_ids = preds[:, 5]
    coeffs = preds[:, 6:]  # Extract the 32 mask coefficients shape: (N, 32)

    # Segmentation Mask Post-Processing
    num_masks = len(preds)
    protos_flat = protos.reshape(32, -1)
    # Linear combination of coefficients and proto maps followed by Sigmoid
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


if __name__ == "__main__":
    boxes, masks = run_inference("yolo26n-seg.onnx", "test.jpg")
    print(f"Detected {len(boxes)} object(s).")
