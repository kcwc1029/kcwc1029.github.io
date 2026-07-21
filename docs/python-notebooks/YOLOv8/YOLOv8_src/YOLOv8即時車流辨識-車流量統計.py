import cv2
from ultralytics import YOLO

url = "https://trafficvideo4.tainan.gov.tw/cdab5ef2"
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(url)

vehicle_classes = [2, 3, 5, 7]

line_y = 350
counted_ids = set()
total_count = 0

while True:

    ret, frame = cap.read()

    if not ret:
        print("讀取影像失敗")
        break

    results = model.track(
        frame,
        conf=0.4,
        classes=vehicle_classes,
        persist=True,
        verbose=False
    )

    annotated = results[0].plot()

    boxes = results[0].boxes

    if boxes.id is not None:

        for box in boxes:

            track_id = int(box.id[0])

            x1, y1, x2, y2 = box.xyxy[0]
            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)

            cv2.circle(
                annotated,
                (center_x, center_y),
                5,
                (0, 255, 255),
                -1
            )

            if center_y > line_y and track_id not in counted_ids:
                counted_ids.add(track_id)
                total_count += 1

    cv2.line(
        annotated,
        (0, line_y),
        (annotated.shape[1], line_y),
        (0, 0, 255),
        2
    )

    cv2.putText(
        annotated,
        f"Total Vehicles: {total_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Traffic Flow Counting", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()