import cv2
import yt_dlp
from ultralytics import YOLO


# =========================
# YouTube 影片網址
# =========================

YOUTUBE_URL = "https://www.youtube.com/watch?v=_vxaPVKe1wE" # "請貼上你的 YouTube 影片網址"

MODEL_PATH = "yolov8n-pose.pt"
OUTPUT_PATH = "baseball_pose_output.mp4"


# =========================
# 取得 YouTube 串流網址
# =========================

def get_youtube_stream_url(youtube_url):
    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info["url"]


# =========================
# 主程式
# =========================

def main():
    print("正在載入 YOLOv8-Pose 模型...")
    model = YOLO(MODEL_PATH)

    print("正在取得 YouTube 影片串流...")
    video_url = get_youtube_stream_url(YOUTUBE_URL)

    cap = cv2.VideoCapture(video_url)

    if not cap.isOpened():
        print("無法開啟影片，請確認 YouTube 網址是否正確")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        OUTPUT_PATH,
        fourcc,
        fps,
        (width, height)
    )

    print("開始進行棒球姿態分析...")
    print("按 q 可以提前結束")

    while True:
        success, frame = cap.read()

        if not success:
            break

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

        cv2.putText(
            annotated_frame,
            f"Players: {people_count}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3
        )

        writer.write(annotated_frame)

        cv2.imshow(
            "YOLOv8-Pose Baseball Analysis",
            annotated_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    writer.release()
    cv2.destroyAllWindows()

    print("分析完成")
    print(f"輸出影片：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()