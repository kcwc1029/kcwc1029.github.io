import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cartoon = cv2.stylization(
        frame,
        sigma_s=100,
        sigma_r=0.3
    )

    cv2.imshow(
        "Cartoon",
        cartoon
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()