import cv2
import csv
import time
from datetime import datetime

import matplotlib.pyplot as plt
from ultralytics import YOLO


url = "https://trafficvideo4.tainan.gov.tw/cdab5ef2"
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(url)

vehicle_classes = [2, 3, 5, 7]

line_y = 350
counted_ids = set()
total_count = 0

csv_path = "traffic_flow.csv"

# 每幾秒記錄一次
record_interval = 10
last_record_time = time.time()

# 區間車流量
last_total_count = 0


# 建立 CSV 檔案，先寫入欄位名稱
with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["time", "interval_seconds", "count", "total_count"])


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

    # 每 10 秒記錄一次 CSV
    current_time = time.time()

    if current_time - last_record_time >= record_interval:

        now_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        interval_count = total_count - last_total_count

        with open(csv_path, mode="a", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([
                now_text,
                record_interval,
                interval_count,
                total_count
            ])

        print(f"{now_text} | 這 {record_interval} 秒通過 {interval_count} 台 | 累積 {total_count} 台")

        last_total_count = total_count
        last_record_time = current_time

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


# 程式結束後，畫出車流趨勢圖
times = []
counts = []

with open(csv_path, mode="r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        times.append(row["time"])
        counts.append(int(row["count"]))

plt.figure(figsize=(12, 5))
plt.plot(times, counts, marker="o")
plt.title("Traffic Flow Trend")
plt.xlabel("Time")
plt.ylabel("Vehicles per Interval")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()