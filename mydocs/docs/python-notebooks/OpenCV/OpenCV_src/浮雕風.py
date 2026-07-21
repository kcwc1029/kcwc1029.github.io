import cv2
import numpy as np

kernel = np.array([
    [-2,-1,0],
    [-1,1,1],
    [0,1,2]
])

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    emboss = cv2.filter2D(
        frame,
        -1,
        kernel
    )

    cv2.imshow(
        "Emboss",
        emboss
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()