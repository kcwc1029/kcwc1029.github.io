### YOLOv8偵測一張街景圖片
from ultralytics import YOLO
import cv2

def resize_image(image, max_width=1200):

    height, width = image.shape[:2]

    if width <= max_width:
        return image

    scale = max_width / width

    return cv2.resize(
        image,
        None,
        fx=scale,
        fy=scale
    )

model = YOLO("yolov8n.pt")

image = cv2.imread("../YOLOv8_datasets/街景照片.png")

results = model.predict(
    image,
    conf=0.4,
    verbose=False
)

for box in results[0].boxes:

    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

    class_id = int(box.cls[0])

    score = float(box.conf[0])

    class_name = model.names[class_id]

    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )

    cv2.putText(
        image,
        f"{class_name} {score:.2f}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

image = resize_image(image)

cv2.imshow(
    "YOLO Detection",
    image
)

cv2.waitKey(0)
cv2.destroyAllWindows()