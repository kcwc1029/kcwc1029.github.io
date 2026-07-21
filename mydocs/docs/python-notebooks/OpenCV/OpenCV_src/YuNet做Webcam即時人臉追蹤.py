from pathlib import Path
from urllib.request import urlretrieve

import cv2


current_file = Path(__file__).resolve()

MODEL_DIR = (
    current_file.parent.parent
    / "OpenCV_datasets"
)

MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "face_detection_yunet_2023mar.onnx"

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

next_id = 1
tracks = {}
max_distance = 80


def get_center(face):
    x, y, fw, fh = face[:4].astype(int)
    return x + fw // 2, y + fh // 2


while True:
    ok, frame = cap.read()

    if not ok:
        break

    h, w = frame.shape[:2]

    detector.setInputSize((w, h))

    _, faces = detector.detect(frame)

    current_centers = []

    if faces is not None:
        for face in faces:
            current_centers.append(
                (face, get_center(face))
            )

    used_ids = set()
    updated_tracks = {}

    for face, center in current_centers:
        cx, cy = center

        best_id = None
        best_distance = max_distance

        for track_id, points in tracks.items():
            if track_id in used_ids:
                continue

            last_x, last_y = points[-1]

            distance = (
                (cx - last_x) ** 2
                + (cy - last_y) ** 2
            ) ** 0.5

            if distance < best_distance:
                best_distance = distance
                best_id = track_id

        if best_id is None:
            best_id = next_id
            next_id += 1

        used_ids.add(best_id)

        old_points = tracks.get(best_id, [])
        new_points = old_points + [center]

        if len(new_points) > 30:
            new_points = new_points[-30:]

        updated_tracks[best_id] = new_points

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
            f"ID {best_id}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    tracks = updated_tracks

    for track_id, points in tracks.items():
        for i in range(1, len(points)):
            cv2.line(
                frame,
                points[i - 1],
                points[i],
                (0, 255, 0),
                2
            )

        if points:
            cv2.circle(
                frame,
                points[-1],
                5,
                (0, 255, 0),
                -1
            )

    cv2.putText(
        frame,
        f"Tracking Faces: {len(tracks)}",
        (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "YuNet webcam face tracking",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()