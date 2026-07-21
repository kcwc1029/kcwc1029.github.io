from pathlib import Path
from urllib.request import urlretrieve

import cv2
import numpy as np


# ==================================================
# 路徑設定
# ==================================================

current_file = Path(__file__).resolve()
BASE_DIR = current_file.parent.parent

MODEL_DIR = BASE_DIR / "OpenCV_datasets"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "face_detection_yunet_2023mar.onnx"


# ==================================================
# YuNet 模型下載
# ==================================================

MODEL_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
    "face_detection_yunet_2023mar.onnx"
)

if not MODEL_PATH.exists():
    print("正在下載 YuNet 模型...")
    print(f"儲存位置：{MODEL_PATH}")

    urlretrieve(MODEL_URL, str(MODEL_PATH))

    print("下載完成")

if MODEL_PATH.stat().st_size < 100000:
    MODEL_PATH.unlink()
    raise RuntimeError("模型檔案異常，請重新執行程式下載")

print(f"模型位置：{MODEL_PATH}")


# ==================================================
# Webcam
# ==================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

ok, frame = cap.read()

if not ok:
    raise RuntimeError("Cannot read webcam frame")

h, w = frame.shape[:2]


# ==================================================
# YuNet 偵測器
# ==================================================

detector = cv2.FaceDetectorYN.create(
    str(MODEL_PATH),
    "",
    (w, h),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)


# ==================================================
# 主程式
# ==================================================

while True:
    ok, frame = cap.read()

    if not ok:
        break

    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    blurred = cv2.GaussianBlur(
        frame,
        (51, 51),
        0
    )

    mask = np.zeros(
        (h, w),
        dtype=np.uint8
    )

    face_count = 0

    if faces is not None:
        face_count = len(faces)

        for face in faces:
            x, y, fw, fh = face[:4].astype(int)

            padding = 50

            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(w, x + fw + padding)
            y2 = min(h, y + fh + padding)

            cv2.rectangle(
                mask,
                (x1, y1),
                (x2, y2),
                255,
                -1
            )

    mask = cv2.GaussianBlur(
        mask,
        (31, 31),
        0
    )

    mask_3ch = cv2.merge(
        [mask, mask, mask]
    ) / 255.0

    output = (
        frame * mask_3ch
        + blurred * (1 - mask_3ch)
    ).astype(np.uint8)

    cv2.putText(
        output,
        f"Faces: {face_count}",
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        output,
        "Face clear, background blurred",
        (25, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "YuNet Webcam Background Blur",
        output
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()