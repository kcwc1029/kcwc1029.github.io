### 只保留人、汽車、機車、公車與卡車。
from ultralytics import YOLO
import cv2




video_path = "../YOLOv8_datasets/8915716-uhd_3840_2160_30fps.mp4"

model = YOLO("yolov8n.pt")

# COCO 類別：0=person、2=car、3=motorcycle、5=bus、7=truck
target_classes = [0, 2, 3, 5, 7]

cap = cv2.VideoCapture(str(video_path))

if not cap.isOpened():
    raise RuntimeError("無法開啟影片")


while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        source=frame,
        classes=target_classes,
        conf=0.4,
        verbose=False
    )

    result = results[0]

    # 把 YOLO 偵測結果畫在 frame 上
    annotated_frame = result.plot()

    annotated_frame = cv2.resize(
        annotated_frame,
        (960, 540)
    )

    cv2.imshow("YOLOv8 Traffic Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()