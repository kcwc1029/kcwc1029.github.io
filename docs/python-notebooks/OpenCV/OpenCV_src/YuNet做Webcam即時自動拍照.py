from pathlib import Path
from urllib.request import urlretrieve
import time

import cv2


# ==================================================
# 路徑設定
# ==================================================

current_file = Path(__file__).resolve()

BASE_DIR = current_file.parent.parent

MODEL_DIR = BASE_DIR / "OpenCV_datasets"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "face_detection_yunet_2023mar.onnx"

OUT_DIR = (
    BASE_DIR
    / "OpenCV_outputs"
    / "auto_capture"
)

OUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


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

    urlretrieve(
        MODEL_URL,
        str(MODEL_PATH)
    )

    print("下載完成")


if MODEL_PATH.stat().st_size < 100000:

    MODEL_PATH.unlink()

    raise RuntimeError(
        "模型檔案異常，請重新執行程式下載"
    )


# ==================================================
# 操作說明
# ==================================================

print("\n" + "=" * 60)
print("YuNet 自動拍照系統")
print("=" * 60)

print(f"模型位置：{MODEL_PATH}")
print(f"照片輸出：{OUT_DIR}")

print("\n功能說明：")
print("1. 偵測到人臉後自動拍照")
print("2. 每隔 3 秒拍一張")
print("3. 照片會儲存到 OpenCV_outputs/auto_capture")
print("4. 按 q 離開程式")

print("=" * 60 + "\n")


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
# YuNet
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
# 自動拍照設定
# ==================================================

last_capture_time = 0

capture_interval = 3

capture_count = 0


# ==================================================
# 主迴圈
# ==================================================

while True:

    ok, frame = cap.read()

    if not ok:
        break

    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    face_count = 0

    now = time.time()

    if faces is not None:

        face_count = len(faces)

        for face in faces:

            x, y, fw, fh = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                (0, 0, 255),
                2
            )

        if now - last_capture_time >= capture_interval:

            capture_count += 1

            filename = (
                OUT_DIR
                / f"capture_{capture_count:03d}.png"
            )

            cv2.imwrite(
                str(filename),
                frame
            )

            print(
                f"[拍照成功] "
                f"{filename.name}"
            )

            last_capture_time = now


    # 人臉數量
    cv2.putText(
        frame,
        f"Faces: {face_count}",
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    # 已拍照數量
    cv2.putText(
        frame,
        f"Captured: {capture_count}",
        (25, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # 說明文字
    cv2.putText(
        frame,
        "Auto Capture Every 3 Seconds",
        (25, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 0),
        2
    )

    cv2.imshow(
        "YuNet Webcam Auto Capture",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()