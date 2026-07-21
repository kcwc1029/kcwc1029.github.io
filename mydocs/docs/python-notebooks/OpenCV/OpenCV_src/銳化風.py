import cv2
import numpy as np

kernel = np.array([
    [0,-1,0],
    [-1,5,-1],
    [0,-1,0]
])

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    sharpen = cv2.filter2D(
        frame,
        -1,
        kernel
    )

    cv2.imshow(
        "Sharpen",
        sharpen
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()