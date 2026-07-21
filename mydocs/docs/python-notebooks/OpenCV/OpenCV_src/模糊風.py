import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    blur = cv2.GaussianBlur(
        frame,
        (31,31),
        0
    )

    cv2.imshow(
        "Blur",
        blur
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()