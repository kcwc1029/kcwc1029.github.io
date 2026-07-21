import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    cv2.imshow(
        "Heatmap",
        heatmap
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()