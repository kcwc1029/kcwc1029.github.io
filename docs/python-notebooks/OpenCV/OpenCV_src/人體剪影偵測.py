import cv2
import numpy as np


# =========================
# 開啟 Webcam
# =========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError("無法開啟攝影機")


background = None


while True:
    ret, frame = cap.read()

    if not ret:
        print("讀不到攝影機畫面")
        break

    # 左右翻轉，畫面比較像照鏡子
    frame = cv2.flip(frame, 1)

    # 複製原始畫面
    result = frame.copy()

    # 轉灰階
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # 模糊，降低雜訊
    gray_blur = cv2.GaussianBlur(
        gray,
        (7, 7),
        0
    )

    text = "Press b to set background"

    if background is not None:

        # =========================
        # 背景相減
        # =========================
        # 比較目前畫面與背景差異
        diff = cv2.absdiff(
            background,
            gray_blur
        )

        # =========================
        # threshold 二值化
        # =========================
        # 差異大的地方變白色
        # 差異小的地方變黑色
        _, mask = cv2.threshold(
            diff,
            30,
            255,
            cv2.THRESH_BINARY
        )

        # =========================
        # 去雜訊
        # =========================
        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        mask = cv2.dilate(
            mask,
            kernel,
            iterations=2
        )

        # =========================
        # 找輪廓
        # =========================
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        silhouette = np.full_like(
            frame,
            255
        )

        if contours:
            # 只取最大輪廓
            # 假設最大物體就是人物
            max_contour = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(max_contour)

            if area > 5000:

                # =========================
                # 建立人物剪影
                # =========================
                # 先建立全白背景
                silhouette = np.full_like(
                    frame,
                    255
                )

                # 把人物輪廓區域填成黑色
                cv2.drawContours(
                    silhouette,
                    [max_contour],
                    -1,
                    (0, 0, 0),
                    thickness=-1
                )

                # 在原圖上畫出人物輪廓
                cv2.drawContours(
                    result,
                    [max_contour],
                    -1,
                    (0, 255, 0),
                    3
                )

                text = "Human Silhouette"

        # 顯示 mask 與剪影
        cv2.imshow("Mask", mask)
        cv2.imshow("Silhouette", silhouette)

    # 顯示提示文字
    cv2.putText(
        result,
        text,
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 255),
        3
    )

    cv2.imshow("Webcam", result)

    key = cv2.waitKey(1) & 0xFF

    # 按 b 記錄背景
    if key == ord("b"):
        background = gray_blur.copy()
        print("背景已記錄，現在可以站進畫面")

    # 按 q 離開
    elif key == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()