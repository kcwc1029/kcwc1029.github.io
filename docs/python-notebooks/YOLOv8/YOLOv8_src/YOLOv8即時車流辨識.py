import cv2
from ultralytics import YOLO

url = "https://trafficvideo4.tainan.gov.tw/cdab5ef2" # 你的車流網址
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(url)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        conf=0.4,
        verbose=False, 
    )

    annotated = results[0].plot()

    cv2.imshow(
        "Traffic Detection",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()