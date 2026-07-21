import cv2

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    sketch_gray, sketch_color = cv2.pencilSketch(
        frame,
        sigma_s=60,
        sigma_r=0.07,
        shade_factor=0.05
    )

    cv2.imshow(
        "Pencil Sketch",
        sketch_gray
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()