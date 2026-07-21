### 範例程式：偵測紅色區域
import cv2
import numpy as np

# 讀取圖片
image = cv2.imread("../OpenCV_datasets/white_fish.png")

if image is None:
    print("圖片讀取失敗，請檢查路徑或檔名")
else:
    # BGR 轉 HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 紅色在 HSV 中會分成兩段範圍
    lower_red_1 = np.array([0, 80, 80])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 80, 80])
    upper_red_2 = np.array([180, 255, 255])

    # 建立紅色遮罩
    mask1 = cv2.inRange(hsv_image, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv_image, lower_red_2, upper_red_2)

    red_mask = mask1 + mask2

    # 只保留紅色區域
    red_result = cv2.bitwise_and(image, image, mask=red_mask)

    cv2.imshow("Original Image", image)
    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Red Result", red_result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()