import cv2
import yt_dlp

from ultralytics import YOLO

youtube_url = "https://youtu.be/0nTO4zSEpOs" # 影片網址

ydl_opts = {
    "format": "best"
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:

    info = ydl.extract_info(
        youtube_url,
        download=False
    )

    stream_url = info["url"]

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(stream_url)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = model.predict(
        frame,
        classes=[0],
        conf=0.4,
        verbose=False
    )

    annotated = results[0].plot()

    people_count = len(
        results[0].boxes
    )

    cv2.putText(
        annotated,
        f"People: {people_count}",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow(
        "YOLOv8 Person Counter",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()