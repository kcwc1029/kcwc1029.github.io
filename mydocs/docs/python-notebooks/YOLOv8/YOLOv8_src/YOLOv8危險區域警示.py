# file_name: yolo_zone_intrusion_webcam.py

import cv2
import numpy as np
from ultralytics import YOLO


# =========================
# 基本設定
# =========================

model = YOLO("yolov8n.pt")

PERSON_CLASS_ID = 0
CONFIDENCE = 0.45

zone_points = []
drawing_done = False
detecting = False


# =========================
# 滑鼠事件：點 4 個點畫禁區
# =========================

def mouse_callback(event, x, y, flags, param):
    global zone_points, drawing_done

    if detecting:
        return

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(zone_points) < 4:
            zone_points.append((x, y))

        if len(zone_points) == 4:
            drawing_done = True


# =========================
# 判斷點是否在多邊形內
# =========================

def point_in_zone(point, zone):
    zone_np = np.array(zone, np.int32)
    result = cv2.pointPolygonTest(zone_np, point, False)
    return result >= 0


# =========================
# 主程式
# =========================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("無法開啟攝影機，請檢查攝影機權限，或把 0 改成 1。")

cv2.namedWindow("YOLOv8 Zone Intrusion Detection")
cv2.setMouseCallback("YOLOv8 Zone Intrusion Detection", mouse_callback)

while True:
    success, frame = cap.read()

    if not success:
        print("讀取攝影機畫面失敗。")
        break

    intrusion_detected = False

    # 畫出已點選的點
    for point in zone_points:
        cv2.circle(frame, point, 6, (0, 255, 255), -1)

    # 畫出禁區
    if len(zone_points) >= 2:
        for i in range(len(zone_points) - 1):
            cv2.line(frame, zone_points[i], zone_points[i + 1], (0, 255, 255), 2)

    if drawing_done:
        zone_np = np.array(zone_points, np.int32)
        cv2.polylines(frame, [zone_np], True, (0, 255, 255), 3)

        overlay = frame.copy()
        cv2.fillPoly(overlay, [zone_np], (0, 255, 255))
        frame = cv2.addWeighted(overlay, 0.25, frame, 0.75, 0)

    # 開始偵測
    if detecting and drawing_done:
        results = model.predict(
            frame,
            conf=CONFIDENCE,
            classes=[PERSON_CLASS_ID],
            verbose=False
        )

        result = results[0]

        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            conf = float(box.conf[0])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            center = (center_x, center_y)

            is_inside = point_in_zone(center, zone_points)

            if is_inside:
                intrusion_detected = True
                box_color = (0, 0, 255)
                text = "INTRUSION"
            else:
                box_color = (0, 255, 0)
                text = "Person"

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.circle(frame, center, 5, box_color, -1)

            cv2.putText(
                frame,
                f"{text} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                box_color,
                2
            )

    # 警示文字
    if intrusion_detected:
        cv2.rectangle(frame, (20, 20), (620, 90), (0, 0, 255), -1)
        cv2.putText(
            frame,
            "WARNING: Someone entered the restricted area!",
            (35, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2
        )

    # 操作提示
    if not drawing_done:
        hint = "Click 4 points to draw restricted zone"
    elif not detecting:
        hint = "Press ENTER to start detection"
    else:
        hint = "Detecting... Press R to reset zone, Q to quit"

    cv2.putText(
        frame,
        hint,
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.imshow("YOLOv8 Zone Intrusion Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == 13:  # Enter
        if drawing_done:
            detecting = True

    if key == ord("r"):
        zone_points = []
        drawing_done = False
        detecting = False

cap.release()
cv2.destroyAllWindows()