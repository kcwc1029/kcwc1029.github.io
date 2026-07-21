### 即時攝影機偵測，按 q 離開

import cv2
from ultralytics import YOLO


model = YOLO("yolov8n.pt")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise RuntimeError("無法開啟攝影機，請檢查權限或將索引 0 改成 1。")


while True:
    success, frame = camera.read()

    if not success:
        print("讀取畫面失敗。")
        break

    result = model.predict(
        frame,
        conf=0.45,
        verbose=False
    )[0]

    annotated_frame = result.plot()

    cv2.imshow(
        "YOLOv8 Webcam Detection - Press q to quit",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()