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
    / "face_crop"
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
print("YuNet 臉部裁切系統")
print("=" * 60)

print(f"模型位置：{MODEL_PATH}")
print(f"輸出位置：{OUT_DIR}")

print("\n功能說明：")
print("1. 即時偵測人臉")
print("2. 按 s 儲存所有人臉")
print("3. 按 q 離開程式")

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


save_count = 0


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

    if faces is not None:

        face_count = len(faces)

        for index, face in enumerate(faces, start=1):

            x, y, fw, fh = face[:4].astype(int)

            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"Face {index}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )


    cv2.putText(
        frame,
        f"Faces: {face_count}",
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"Saved: {save_count}",
        (25, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Press S to Save Face Crop",
        (25, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Press Q to Quit",
        (25, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "YuNet Webcam Face Crop",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # ==========================================
    # 儲存人臉
    # ==========================================

    if key == ord("s"):

        if faces is None:

            print("未偵測到人臉")

        else:

            timestamp = int(time.time())

            for index, face in enumerate(faces, start=1):

                x, y, fw, fh = face[:4].astype(int)

                x1 = max(0, x)
                y1 = max(0, y)

                x2 = min(w, x + fw)
                y2 = min(h, y + fh)

                face_img = frame[
                    y1:y2,
                    x1:x2
                ]

                if face_img.size == 0:
                    continue

                filename = (
                    OUT_DIR
                    / f"face_{timestamp}_{index}.png"
                )

                cv2.imwrite(
                    str(filename),
                    face_img
                )

                save_count += 1

                print(
                    f"[儲存成功] "
                    f"{filename.name}"
                )

    # ==========================================
    # 離開程式
    # ==========================================

    if key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()