import time

import cv2
import yt_dlp
from ultralytics import YOLO


# =========================
# YouTube 直播網址
# =========================

YOUTUBE_URL = "https://www.youtube.com/watch?v=aVAO2wSUsPo"

MODEL_PATH = "yolov8n-pose.pt"


# =========================
# 取得 YouTube 真正串流網址
# =========================

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            youtube_url,
            download=False
        )

        return info["url"]


# =========================
# 主程式
# =========================

def main():
    print("正在載入 YOLOv8-Pose 模型...")
    model = YOLO(MODEL_PATH)

    print("正在取得 YouTube 直播串流...")
    stream_url = get_youtube_stream_url(YOUTUBE_URL)

    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("無法開啟直播串流")
        print("請確認 YouTube 網址是否正確，或直播是否仍然存在")
        return

    print("開始辨識街景直播")
    print("按 q 離開")

    while True:
        start_time = time.time()

        success, frame = cap.read()

        if not success:
            print("讀取直播畫面失敗，重新連線中...")
            cap.release()
            time.sleep(2)

            stream_url = get_youtube_stream_url(YOUTUBE_URL)
            cap = cv2.VideoCapture(stream_url)
            continue

        results = model.predict(
            frame,
            conf=0.45,
            verbose=False
        )

        result = results[0]
        annotated_frame = result.plot()

        people_count = 0

        if result.boxes is not None:
            people_count = len(result.boxes)

        end_time = time.time()
        fps = 1 / (end_time - start_time)

        cv2.rectangle(
            annotated_frame,
            (10, 10),
            (230, 95),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.2f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            annotated_frame,
            f"People: {people_count}",
            (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            annotated_frame,
            "Status: Running",
            (20, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "YOLOv8-Pose YouTube Live",
            annotated_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()