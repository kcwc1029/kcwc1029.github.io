import cv2
import yt_dlp

from ultralytics import YOLO

youtube_url = "https://youtu.be/-ms9uJ1MW64" # 影片網址

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

    results = model.track(
        frame,
        classes=[0,32,34],
        persist=True,
        conf=0.3,
        verbose=False
    )

    annotated = results[0].plot()

    people_count = 0

    for box in results[0].boxes:

        if int(box.cls[0]) == 0:
            people_count += 1

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
        "YOLOv8 Baseball Analysis",
        annotated
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()