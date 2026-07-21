import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    small = cv2.resize(
        frame,
        None,
        fx=0.08,
        fy=0.08
    )

    mosaic = cv2.resize(
        small,
        (frame.shape[1], frame.shape[0]),
        interpolation=cv2.INTER_NEAREST
    )

    cv2.imshow(
        "Mosaic",
        mosaic
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()