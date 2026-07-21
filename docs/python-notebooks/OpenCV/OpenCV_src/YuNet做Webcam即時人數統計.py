from pathlib import Path
from urllib.request import urlretrieve

import cv2


### 取得目前程式位置
current_file = Path(__file__).resolve()


### OpenCV_datasets 資料夾
MODEL_DIR = (
    current_file.parent.parent
    / "OpenCV_datasets"
)

MODEL_DIR.mkdir(exist_ok=True)


### 模型檔路徑
MODEL_PATH = (
    MODEL_DIR
    / "face_detection_yunet_2023mar.onnx"
)


### 模型下載網址
MODEL_URL = (
    "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/"
    "face_detection_yunet_2023mar.onnx"
)


### 自動下載模型
if not MODEL_PATH.exists():

    print("正在下載 YuNet 模型...")
    print(f"儲存位置：{MODEL_PATH}")

    urlretrieve(
        MODEL_URL,
        str(MODEL_PATH)
    )

    print("下載完成")


### 檢查模型是否正常
if MODEL_PATH.stat().st_size < 100000:

    MODEL_PATH.unlink()

    raise RuntimeError(
        "模型檔案異常，請重新執行程式下載"
    )


print(f"模型位置：{MODEL_PATH}")


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")


ok, frame = cap.read()

if not ok:
    raise RuntimeError("Cannot read webcam frame")


h, w = frame.shape[:2]


detector = cv2.FaceDetectorYN.create(
    str(MODEL_PATH),
    "",
    (w, h),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)


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

        for face in faces:

            x, y, fw, fh = face[:4].astype(int)

            score = face[-1]

            cv2.rectangle(
                frame,
                (x, y),
                (x + fw, y + fh),
                (0, 0, 255),
                2
            )

            cv2.putText(
                frame,
                f"{score:.2f}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

    cv2.putText(
        frame,
        f"faces: {face_count}",
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    cv2.imshow(
        "YuNet webcam face detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()