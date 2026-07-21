import cv2
import numpy as np


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法開啟 Webcam")
    raise SystemExit


print("Webcam 背景去除")
print("按 q 離開程式")

while True:
    ret, frame = cap.read()

    if not ret:
        print("無法讀取畫面")
        break

    # 左右翻轉，比較像照鏡子
    frame = cv2.flip(frame, 1)

    # 轉 HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 假設背景偏白或偏亮
    lower_white = np.array([0, 0, 160])
    upper_white = np.array([180, 80, 255])

    # 找出背景
    background_mask = cv2.inRange(
        hsv,
        lower_white,
        upper_white
    )

    # 反相，取得前景
    foreground_mask = cv2.bitwise_not(background_mask)

    # 去除雜訊
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

    # 建立黑色背景
    black_background = np.zeros_like(frame)

    # 合成結果
    result = np.where(
        foreground_mask[:, :, None] == 255,
        frame,
        black_background
    )

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", foreground_mask)
    cv2.imshow("Background Removed", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()