import cv2
import numpy as np


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法開啟 Webcam")
    raise SystemExit


print("Webcam 背景模糊")
print("按 q 離開程式")

while True:
    ret, frame = cap.read()

    if not ret:
        print("無法讀取畫面")
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 160])
    upper_white = np.array([180, 80, 255])

    background_mask = cv2.inRange(
        hsv,
        lower_white,
        upper_white
    )

    foreground_mask = cv2.bitwise_not(background_mask)

    kernel = np.ones((5, 5), np.uint8)

    foreground_mask = cv2.morphologyEx(
        foreground_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    foreground_mask = cv2.morphologyEx(
        foreground_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # 模糊整張畫面
    blurred = cv2.GaussianBlur(
        frame,
        (51, 51),
        0
    )

    # 人物保留原圖，背景使用模糊圖
    result = np.where(
        foreground_mask[:, :, None] == 255,
        frame,
        blurred
    )

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", foreground_mask)
    cv2.imshow("Background Blur", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()