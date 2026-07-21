"""使用 webcam 即時統計畫面中的人數並輸出 CSV 與影片"""

import csv
import time

import cv2
from ultralytics import YOLO


# 載入模型
model = YOLO("yolov8n.pt")

# 開啟 webcam
capture = cv2.VideoCapture(0)

if not capture.isOpened():
    raise RuntimeError("無法開啟 webcam")


# 取得 webcam 資訊
fps = 30

width = int(
    capture.get(cv2.CAP_PROP_FRAME_WIDTH)
)

height = int(
    capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
)


# 建立影片輸出器
video_writer = cv2.VideoWriter(
    "../YOLOv8_outputs/people_count.mp4",
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height),
)

rows = []

start_time = time.time()
last_record_second = -1

while True:

    success, frame = capture.read()

    if not success:
        break

    # COCO 類別 0 = person
    result = model.predict(
        frame,
        classes=[0],
        conf=0.4,
        verbose=False,
    )[0]

    people_count = len(result.boxes)

    annotated = result.plot()

    cv2.putText(
        annotated,
        f"People: {people_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 255),
        3,
    )

    current_second = int(
        time.time() - start_time
    )

    # 每秒紀錄一次
    if current_second != last_record_second:

        print(
            f"{current_second} 秒：{people_count} 人"
        )

        rows.append(
            {
                "秒數": current_second,
                "偵測人數": people_count,
            }
        )

        last_record_second = current_second

    # 寫入影片
    video_writer.write(
        annotated
    )

    cv2.imshow(
        "People Counter",
        annotated,
    )

    # 按 q 離開
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


capture.release()
video_writer.release()

cv2.destroyAllWindows()


# 輸出 CSV
with open(
    "../YOLOv8_outputs/people_count.csv",
    "w",
    newline="",
    encoding="utf-8-sig",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "秒數",
            "偵測人數",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)

print("CSV 已儲存：people_count.csv")
print("影片已儲存：people_count.mp4")